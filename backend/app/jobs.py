"""Temporary job lifecycle, one worker, cancellation and safe cleanup."""

import queue
import secrets
import shutil
import sqlite3
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from filelock import FileLock

from .config import settings
from .images import OpenAIProvider
from .media import render
from .models import Design, TranscriptionOptions

ACTIVE = {"queued", "transcribing", "generating_image", "rendering_preview", "rendering_video", "cancelling"}


@dataclass
class Job:
    """Hold one temporary episode, its files, state, approvals and cancellation resources."""

    id: str
    token: str
    path: Path
    meta: dict
    cues: list
    warnings: list
    design: Design = field(default_factory=Design)
    state: str = "ready"
    phase: str = "Listo para diseñar"
    progress: float | None = None
    error: str | None = None
    expires: float = field(default_factory=lambda: time.time() + settings.ttl_seconds)
    active_deadline: float = 0
    approved: bool = False
    preview_approved: bool = False
    artifacts: set = field(default_factory=lambda: {"background"})
    background_mode: str = "local"
    cancel: threading.Event = field(default_factory=threading.Event)
    process: object = None
    readers: int = 0
    deleting: bool = False
    subtitle_source: str = "upload"
    subtitles_approved: bool = True
    transcription_options: TranscriptionOptions = field(default_factory=TranscriptionOptions)
    project_id: str | None = None
    archive_error: str | None = None

    def public(self):
        """Return the token-free job snapshot exposed by status polling."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "archive_error": self.archive_error,
            "state": self.state,
            "phase": self.phase,
            "progress": self.progress,
            "error": self.error,
            "metadata": self.meta,
            "warnings": self.warnings,
            "config": self.design.model_dump(),
            "background_approved": self.approved,
            "preview_approved": self.preview_approved,
            "background_mode": self.background_mode,
            "artifacts": sorted(self.artifacts),
            "subtitle_source": self.subtitle_source,
            "subtitles_ready": bool(self.cues),
            "subtitles_approved": self.subtitles_approved,
            "word_timestamps": any(c.words for c in self.cues),
            "expires_at": datetime.fromtimestamp(
                self.active_deadline if self.state in ACTIVE else self.expires, UTC
            ).isoformat(),
        }


class Store:
    """Own the in-memory registry, locks, bounded queue, worker and managed cleanup."""

    def __init__(self):
        """Initialize the instance resources; background threads are started separately."""
        self.jobs = {}
        self.lock = threading.RLock()
        self.queue = queue.Queue(maxsize=settings.queue_size)
        self.stop = threading.Event()
        self.root = settings.temp_root.resolve()
        self.provider = OpenAIProvider()

    def start(self):
        """Lock the exclusive temporary root, remove stale managed jobs and start worker/cleaner threads."""
        self.root.mkdir(parents=True, exist_ok=True)
        if settings.temp_root.is_symlink():
            raise RuntimeError("TEMP_ROOT no puede ser un enlace simbólico.")
        marker = self.root / ".easypodcast-root"
        if not marker.exists() and any(self.root.iterdir()):
            raise RuntimeError("TEMP_ROOT debe ser una carpeta vacía exclusiva de EasyPodcast.")
        marker.touch()
        self.file_lock = FileLock(str(self.root / ".instance.lock"), thread_local=False)
        self.file_lock.acquire(timeout=0)
        for path in self.root.iterdir():
            if len(path.name) == 32 and all(c in "0123456789abcdef" for c in path.name):
                self.remove_path(path)
        self.worker = threading.Thread(target=self.work, daemon=True)
        self.cleaner = threading.Thread(target=self.clean_loop, daemon=True)
        self.worker.start()
        self.cleaner.start()

    def close(self):
        """Request cancellation, join background threads and release managed resources and the root lock."""
        self.stop.set()
        with self.lock:
            for job in self.jobs.values():
                job.cancel.set()
        self.worker.join(timeout=210)  # Provider timeout is bounded, no automatic retry.
        self.cleaner.join(timeout=5)
        with self.lock:
            for job in list(self.jobs.values()):
                if not job.readers:
                    self.remove_path(job.path)
        self.file_lock.release()

    def remove_path(self, path):
        """Remove only a direct managed child, without following a symbolic link."""
        if path.parent != self.root:
            raise RuntimeError("Ruta fuera de la raíz administrada.")
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    def new_path(self):
        """Create a UUID-named directory and return its ID and path."""
        jid = uuid.uuid4().hex
        path = self.root / jid
        path.mkdir()
        return jid, path

    def enqueue(self, job, kind, start=0):
        """Queue a copied Design snapshot after checking busy and queue-capacity constraints."""
        with self.lock:
            if job.state in ACTIVE or job.readers:
                raise ValueError("El trabajo está ocupado o tiene una descarga activa.")
            if self.queue.full():
                raise ValueError("La cola está llena; inténtalo cuando termine otro trabajo.")
            job.cancel.clear()
            job.state, job.phase, job.error = "queued", "En cola", None
            job.progress = None
            job.active_deadline = time.time() + settings.active_ttl_seconds
            self.queue.put_nowait((job.id, kind, start, job.design.model_copy(deep=True)))

    def checkpoint(self, job):
        """Keep a durable recovery copy; expose save failures instead of hiding them."""
        from .library import checkpoint

        try:
            with self.lock:
                checkpoint(job)
            job.archive_error = None
        except (OSError, ValueError, sqlite3.Error):
            job.archive_error = (
                "Project recovery copy could not be saved. Check disk space and library access."
            )

    def invalidate(self, job):
        """Discard preview/video artifacts and clear approval after a design or input change."""
        for kind in ("preview", "video"):
            job.artifacts.discard(kind)
            (job.path / f"{kind}.mp4").unlink(missing_ok=True)
        job.preview_approved = False

    def work(self):
        """Consume queued operations serially, publish validated artifacts and update retention/state."""
        while not self.stop.is_set():
            try:
                jid, kind, start, design = self.queue.get(timeout=0.3)
            except queue.Empty:
                continue
            job = self.jobs.get(jid)
            if not job:
                self.queue.task_done()
                continue
            output = job.path / ("generated.png" if kind == "background" else f"{kind}.partial.mp4")
            try:
                with self.lock:
                    if job.cancel.is_set() or job.deleting:
                        raise InterruptedError()
                    job.state = {
                        "transcript": "transcribing",
                        "background": "generating_image",
                        "preview": "rendering_preview",
                        "video": "rendering_video",
                    }[kind]
                    job.phase = {
                        "transcript": "Transcribiendo audio localmente",
                        "background": "Generando imagen",
                        "preview": "Renderizando prueba",
                        "video": "Renderizando episodio",
                    }[kind]
                    if kind == "transcript":
                        self.invalidate(job)
                        job.subtitles_approved = False
                    elif kind == "background":
                        self.invalidate(job)
                    else:
                        job.artifacts.discard(kind)
                        if kind == "preview":
                            job.preview_approved = False
                if kind == "transcript":
                    from .transcription import transcribe

                    cues, srt = transcribe(job)
                elif kind == "background":
                    self.provider.generate_background(design, output)
                else:
                    duration = (
                        min(20, job.meta["duration"] - start) if kind == "preview" else job.meta["duration"]
                    )
                    render(job, design, start, duration, output, lambda p: setattr(job, "progress", p))
                with self.lock:
                    if job.cancel.is_set():
                        raise InterruptedError()
                    if kind == "transcript":
                        (job.path / "generated.srt").write_text(srt, encoding="utf-8")
                        job.cues = cues
                        job.artifacts.add("subtitles")
                        job.warnings = [
                            "Transcripción automática: revisa texto y tiempos estimados antes de continuar."
                        ]
                    else:
                        output.replace(
                            job.path / ("background.png" if kind == "background" else f"{kind}.mp4")
                        )
                        job.artifacts.add(kind)
                    if kind == "background":
                        (job.path / "background-source.png").unlink(missing_ok=True)
                        job.background_mode, job.approved = "openai", False
                    job.state, job.phase = (
                        "completed",
                        "Revisa los subtítulos generados" if kind == "transcript" else "Operación completada",
                    )
                    job.progress = None if kind == "background" else 1.0
                    job.expires = time.time() + settings.ttl_seconds
            except InterruptedError:
                with self.lock:
                    job.state, job.phase, job.progress = "cancelled", "Cancelado; puedes reintentar", None
                    job.expires = time.time() + settings.failure_ttl_seconds
            except Exception as exc:
                with self.lock:
                    job.state, job.phase, job.progress = "failed", "La operación falló", None
                    job.error = (
                        str(exc) if isinstance(exc, ValueError) else "Error interno al procesar el trabajo."
                    )
                    job.expires = time.time() + settings.failure_ttl_seconds
            finally:
                output.unlink(missing_ok=True)
                self.checkpoint(job)
                self.queue.task_done()

    def clean_loop(self):
        """Periodically request cleanup until shutdown is signalled."""
        while not self.stop.wait(2):
            self.cleanup()

    def cleanup(self):
        """Cancel overdue active jobs and remove expired/deleted idle jobs without active readers."""
        now = time.time()
        with self.lock:
            for jid, job in list(self.jobs.items()):
                if job.state in ACTIVE:
                    if job.deleting or now > job.active_deadline:
                        job.cancel.set()
                        job.state = "cancelling"
                elif (job.deleting or now > job.expires) and not job.readers:
                    self.remove_path(job.path)
                    del self.jobs[jid]


store = Store()


def make_job(jid, path, meta, cues, warnings):
    """Construct a temporary job with a random token and initial validated metadata."""
    return Job(jid, secrets.token_urlsafe(32), path, meta, cues, warnings)
