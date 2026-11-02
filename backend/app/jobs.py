import queue
import secrets
import shutil
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
from .models import Design

ACTIVE = {"queued", "generating_image", "rendering_preview", "rendering_video", "cancelling"}


@dataclass
class Job:
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

    def public(self):
        return {
            "id": self.id,
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
            "expires_at": datetime.fromtimestamp(
                self.active_deadline if self.state in ACTIVE else self.expires, UTC
            ).isoformat(),
        }


class Store:
    def __init__(self):
        self.jobs = {}
        self.lock = threading.RLock()
        self.queue = queue.Queue(maxsize=settings.queue_size)
        self.stop = threading.Event()
        self.root = settings.temp_root.resolve()
        self.provider = OpenAIProvider()

    def start(self):
        self.root.mkdir(parents=True, exist_ok=True)
        if settings.temp_root.is_symlink():
            raise RuntimeError("TEMP_ROOT no puede ser un enlace simbólico.")
        marker = self.root / ".easypodcast-root"
        if not marker.exists() and any(self.root.iterdir()):
            raise RuntimeError("TEMP_ROOT debe ser una carpeta vacía exclusiva de EasyPodcast.")
        marker.touch()
        self.file_lock = FileLock(str(self.root / ".instance.lock"))
        self.file_lock.acquire(timeout=0)
        for path in self.root.iterdir():
            if len(path.name) == 32 and all(c in "0123456789abcdef" for c in path.name):
                self.remove_path(path)
        self.worker = threading.Thread(target=self.work, daemon=True)
        self.cleaner = threading.Thread(target=self.clean_loop, daemon=True)
        self.worker.start()
        self.cleaner.start()

    def close(self):
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
        if path.parent != self.root:
            raise RuntimeError("Ruta fuera de la raíz administrada.")
        if path.is_symlink():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)

    def new_path(self):
        jid = uuid.uuid4().hex
        path = self.root / jid
        path.mkdir()
        return jid, path

    def enqueue(self, job, kind, start=0):
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

    def invalidate(self, job):
        for kind in ("preview", "video"):
            job.artifacts.discard(kind)
            (job.path / f"{kind}.mp4").unlink(missing_ok=True)
        job.preview_approved = False

    def work(self):
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
                        "background": "generating_image",
                        "preview": "rendering_preview",
                        "video": "rendering_video",
                    }[kind]
                    job.phase = {
                        "background": "Generando imagen",
                        "preview": "Renderizando prueba",
                        "video": "Renderizando episodio",
                    }[kind]
                    if kind == "background":
                        self.invalidate(job)
                    else:
                        job.artifacts.discard(kind)
                        if kind == "preview":
                            job.preview_approved = False
                if kind == "background":
                    self.provider.generate_background(design, output)
                else:
                    duration = (
                        min(20, job.meta["duration"] - start) if kind == "preview" else job.meta["duration"]
                    )
                    render(job, design, start, duration, output, lambda p: setattr(job, "progress", p))
                with self.lock:
                    if job.cancel.is_set():
                        raise InterruptedError()
                    output.replace(job.path / ("background.png" if kind == "background" else f"{kind}.mp4"))
                    job.artifacts.add(kind)
                    if kind == "background":
                        job.background_mode, job.approved = "openai", False
                    job.state, job.phase = "completed", "Operación completada"
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
                self.queue.task_done()

    def clean_loop(self):
        while not self.stop.wait(2):
            self.cleanup()

    def cleanup(self):
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
    return Job(jid, secrets.token_urlsafe(32), path, meta, cues, warnings)
