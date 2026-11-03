"""Durable local projects and brand templates, separate from disposable render workspaces."""

import json
import secrets
import shutil
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from fastapi import HTTPException
from PIL import Image

from .config import settings
from .models import Design, TranscriptionOptions
from .subtitles import Cue, Word

LOCK = threading.RLock()
FILES = (
    "audio.bin",
    "background.png",
    "background-source.png",
    "logo.png",
    "original.srt",
    "generated.srt",
    "preview.mp4",
    "video.mp4",
)


def root():
    """Prepare an exclusive persistent directory; never reuse an unrelated populated folder."""
    directory = settings.library_root.expanduser().absolute()
    if directory.resolve().is_relative_to(Path(__file__).resolve().parents[2]):
        raise ValueError("Library must be outside the source repository.")
    if directory.is_symlink():
        raise ValueError("Library directory cannot be a symbolic link.")
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    marker = directory / ".easypodcast-library"
    if not marker.exists() and any(directory.iterdir()):
        raise ValueError("Library directory must be empty or an existing EasyPodcast library.")
    marker.touch(exist_ok=True)
    return directory


@contextmanager
def database():
    """Open a short-lived SQLite connection; callers serialize file/database changes with LOCK."""
    path = root() / "library.sqlite3"
    if path.is_symlink():
        raise ValueError("Library database cannot be a symbolic link.")
    connection = sqlite3.connect(path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute(
        "CREATE TABLE IF NOT EXISTS projects (id TEXT PRIMARY KEY, title TEXT, created REAL, updated REAL, state TEXT, snapshot TEXT, draft TEXT)"
    )
    connection.execute(
        "CREATE TABLE IF NOT EXISTS templates (id TEXT PRIMARY KEY, title TEXT, updated REAL, design TEXT)"
    )
    connection.commit()
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def owner_key():
    """Return a machine-local library capability; it is never placed in localStorage or URLs."""
    with LOCK:
        path = root() / ".owner-key"
        if path.is_symlink():
            raise ValueError("Library capability cannot be a symbolic link.")
        if not path.exists():
            path.write_text(secrets.token_urlsafe(48), encoding="utf-8")
            path.chmod(0o600)
        return path.read_text(encoding="utf-8")


def authorize(request):
    """Require the HttpOnly local-library session established by an origin-checked POST."""
    if not secrets.compare_digest(request.cookies.get("ep_library", ""), owner_key()):
        raise HTTPException(401, "Open the local library session first.")


def directory(kind, identifier):
    """Resolve only UUID child directories inside an allowlisted library collection."""
    if (
        kind not in ("projects", "templates")
        or len(identifier) != 32
        or any(c not in "0123456789abcdef" for c in identifier)
    ):
        raise HTTPException(404, "Saved item not found.")
    parent = root() / kind
    if parent.is_symlink():
        raise ValueError("Library collection cannot be a symbolic link.")
    parent.mkdir(exist_ok=True, mode=0o700)
    target = parent / identifier
    if target.is_symlink():
        raise ValueError("Saved item cannot be a symbolic link.")
    target.mkdir(exist_ok=True, mode=0o700)
    return target


def copy_file(source, target):
    """Publish one copied media file atomically without reading its entire contents into memory."""
    if source.is_symlink() or target.is_symlink():
        raise ValueError("Library media cannot be a symbolic link.")
    if shutil.disk_usage(target.parent).free < source.stat().st_size + settings.min_free_bytes:
        raise ValueError("Insufficient disk space to save the project.")
    partial = target.with_name(uuid.uuid4().hex + ".partial")
    try:
        shutil.copy2(source, partial)
        partial.replace(target)
    finally:
        partial.unlink(missing_ok=True)


def checkpoint(job):
    """Save metadata and changed media; never serialize job tokens, thread events or subprocesses."""
    with LOCK:
        if not (job.path / "audio.bin").is_file() or not (job.path / "background.png").is_file():
            raise ValueError("Required project input is missing; the previous recovery copy was retained.")
        identifier = job.project_id or uuid.uuid4().hex
        job.project_id = identifier
        target = directory("projects", identifier)
        with database() as connection:
            existing = connection.execute(
                "SELECT snapshot FROM projects WHERE id=?", (identifier,)
            ).fetchone()
            previous = json.loads(existing["snapshot"]) if existing else {}
            fingerprints = previous.get("files", {})
            for name in FILES:
                source = job.path / name
                if not source.is_file():
                    fingerprints.pop(name, None)
                    continue
                stamp = [source.stat().st_size, source.stat().st_mtime_ns]
                if fingerprints.get(name) != stamp or not (target / name).exists():
                    copy_file(source, target / name)
                    if name == "background.png":
                        with Image.open(source) as image:
                            image.thumbnail((320, 180))
                            image.convert("RGB").save(target / "thumbnail.png")
                fingerprints[name] = stamp
            snapshot = {
                "schema_version": 1,
                "metadata": job.meta,
                "warnings": job.warnings,
                "config": job.design.model_dump(),
                "cues": [
                    {
                        "start": c.start,
                        "end": c.end,
                        "text": c.text,
                        "words": [w.model_dump() for w in c.words],
                        "word_offset": c.word_offset,
                    }
                    for c in job.cues
                ],
                "artifacts": sorted(job.artifacts),
                "background_mode": job.background_mode,
                "background_approved": job.approved,
                "preview_approved": job.preview_approved,
                "subtitle_source": job.subtitle_source,
                "subtitles_approved": job.subtitles_approved,
                "transcription_options": job.transcription_options.model_dump(),
                "files": fingerprints,
            }
            now = time.time()
            connection.execute(
                "INSERT INTO projects VALUES (?,?,?,?,?,?,NULL) ON CONFLICT(id) DO UPDATE SET title=excluded.title,updated=excluded.updated,state=excluded.state,snapshot=excluded.snapshot",
                (identifier, job.design.title, now, now, job.state, json.dumps(snapshot)),
            )
        return identifier


def projects():
    """List durable project summaries without secrets or local filesystem paths."""
    with LOCK, database() as connection:
        return [
            dict(row)
            for row in connection.execute(
                "SELECT id,title,created,updated,state,(draft IS NOT NULL) AS has_draft FROM projects ORDER BY updated DESC"
            )
        ]


def project(identifier):
    """Read a known project record before resolving any media paths."""
    with LOCK, database() as connection:
        row = connection.execute("SELECT * FROM projects WHERE id=?", (identifier,)).fetchone()
        if not row:
            raise HTTPException(404, "Saved project not found.")
        return dict(row)


def save_draft(identifier, design, base):
    """Persist a validated draft without silently approving it or modifying an active render."""
    with LOCK, database() as connection:
        record = project(identifier)
        if json.loads(record["snapshot"])["config"] != base.model_dump():
            return False
        connection.execute(
            "UPDATE projects SET draft=?,updated=? WHERE id=?",
            (design.model_dump_json(), time.time(), identifier),
        )
        return True


def restore(identifier, store, duplicate=False):
    """Create a fresh temporary job/token from durable files; interrupted operations never auto-restart."""
    from .jobs import make_job

    with LOCK:
        row = project(identifier)
        saved = json.loads(row["snapshot"])
        if saved.get("schema_version", 1) != 1:
            raise ValueError("Unsupported saved project version.")
        source = directory("projects", identifier)
        jid, target = store.new_path()
        try:
            for name in saved["files"]:
                if duplicate and name in ("preview.mp4", "video.mp4"):
                    continue
                if name not in FILES:
                    raise ValueError("Saved project contains an unsupported media filename.")
                copy_file(source / name, target / name)
            cues = [
                Cue(
                    c["start"],
                    c["end"],
                    c["text"],
                    tuple(Word.model_validate(w) for w in c["words"]),
                    c.get("word_offset", 0),
                )
                for c in saved["cues"]
            ]
            job = make_job(jid, target, saved["metadata"], cues, saved["warnings"])
            job.design = (
                Design.model_validate_json(row["draft"])
                if row["draft"]
                else Design.model_validate(saved["config"])
            )
            job.project_id = None if duplicate else identifier
            job.artifacts = set(saved["artifacts"])
            job.background_mode = saved["background_mode"]
            job.approved = saved["background_approved"]
            job.preview_approved = saved["preview_approved"]
            job.subtitle_source = saved["subtitle_source"]
            job.subtitles_approved = saved["subtitles_approved"]
            job.transcription_options = TranscriptionOptions.model_validate(saved["transcription_options"])
            job.phase = "Project recovered. Review the design before continuing."
            if row["draft"] and job.design.model_dump() != saved["config"]:
                store.invalidate(job)
            if duplicate:
                job.design.title = (job.design.title[:110] + " (copy)")[:120]
                store.invalidate(job)
            store.jobs[jid] = job
            checkpoint(job)
            clear_draft(job.project_id)
            return job
        except BaseException:
            store.jobs.pop(jid, None)
            store.remove_path(target)
            raise


def save_template(job, title):
    """Save brand settings plus reusable background/logo, without copying source audio or subtitles."""
    with LOCK:
        identifier = uuid.uuid4().hex
        target = directory("templates", identifier)
        for name in ("background.png", "background-source.png", "logo.png"):
            source = job.path / name
            if source.exists():
                copy_file(source, target / name)
        with database() as connection:
            connection.execute(
                "INSERT INTO templates VALUES (?,?,?,?)",
                (identifier, title, time.time(), job.design.model_dump_json()),
            )
        return identifier


def templates():
    """List brand presets without returning their media paths."""
    with LOCK, database() as connection:
        return [
            dict(row)
            for row in connection.execute("SELECT id,title,updated FROM templates ORDER BY updated DESC")
        ]


def apply_template(job, identifier, store):
    """Reuse a brand template, retaining this episode's title and transcription content."""
    with LOCK, database() as connection:
        row = connection.execute("SELECT * FROM templates WHERE id=?", (identifier,)).fetchone()
        if not row:
            raise HTTPException(404, "Brand template not found.")
        design = Design.model_validate_json(row["design"])
        design.title, design.description = job.design.title, job.design.description
        design.trim_subtitles = job.design.trim_subtitles
        design.crf, design.preset = job.design.crf, job.design.preset
        source = directory("templates", identifier)
        for name in ("background.png", "background-source.png", "logo.png"):
            if (source / name).exists():
                copy_file(source / name, job.path / name)
                if name == "logo.png":
                    job.artifacts.add("logo")
        if not (source / "logo.png").exists():
            (job.path / "logo.png").unlink(missing_ok=True)
            job.artifacts.discard("logo")
        if not (source / "background-source.png").exists():
            (job.path / "background-source.png").unlink(missing_ok=True)
        job.design = design
        job.background_mode = "upload"
        job.approved = False
        store.invalidate(job)
        checkpoint(job)


def clear_draft(identifier):
    """Remove a recovery draft only after its configuration was explicitly saved."""
    with LOCK, database() as connection:
        connection.execute("UPDATE projects SET draft=NULL WHERE id=?", (identifier,))
