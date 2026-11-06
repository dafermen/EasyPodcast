"""Durable local projects and brand templates, separate from disposable render workspaces."""

import hashlib
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
    if directory.is_symlink() or directory.is_junction():
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
    for table, additions in {
        "projects": {
            "display_name": "TEXT",
            "deleted_at": "REAL",
            "subtitle_draft": "TEXT",
            "subtitle_version": "INTEGER NOT NULL DEFAULT 0",
        },
        "templates": {"deleted_at": "REAL"},
    }.items():
        columns = {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}
        for name, definition in additions.items():
            if name not in columns:
                connection.execute(f"ALTER TABLE {table} ADD COLUMN {name} {definition}")
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
    if parent.is_symlink() or parent.is_junction():
        raise ValueError("Library collection cannot be a symbolic link.")
    parent.mkdir(exist_ok=True, mode=0o700)
    target = parent / identifier
    if target.is_symlink() or target.is_junction():
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
        with database() as connection:
            existing = connection.execute(
                "SELECT snapshot,deleted_at FROM projects WHERE id=?", (identifier,)
            ).fetchone()
            if existing and existing["deleted_at"] is not None:
                raise ValueError("Project is in Trash. Restore it before editing.")
            target = directory("projects", identifier)
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
                "INSERT INTO projects (id,title,created,updated,state,snapshot,draft) VALUES (?,?,?,?,?,?,NULL) ON CONFLICT(id) DO UPDATE SET title=excluded.title,updated=excluded.updated,state=excluded.state,snapshot=excluded.snapshot",
                (identifier, job.design.title, now, now, job.state, json.dumps(snapshot)),
            )
        return identifier


def projects():
    """List durable project summaries without secrets or local filesystem paths."""
    with LOCK, database() as connection:
        return [
            {**dict(row), "bytes": item_bytes("projects", row["id"])}
            for row in connection.execute(
                "SELECT id,COALESCE(display_name,title) AS title,created,updated,state,(draft IS NOT NULL OR subtitle_draft IS NOT NULL) AS has_draft FROM projects WHERE deleted_at IS NULL ORDER BY updated DESC"
            )
        ]


def project(identifier):
    """Read a known project record before resolving any media paths."""
    with LOCK, database() as connection:
        row = connection.execute(
            "SELECT * FROM projects WHERE id=? AND deleted_at IS NULL", (identifier,)
        ).fetchone()
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
            job.subtitle_draft_available = bool(row["subtitle_draft"])
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
            if duplicate and row["subtitle_draft"]:
                with database() as connection:
                    connection.execute(
                        "UPDATE projects SET subtitle_draft=?,subtitle_version=? WHERE id=?",
                        (row["subtitle_draft"], row["subtitle_version"], job.project_id),
                    )
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
                "INSERT INTO templates (id,title,updated,design) VALUES (?,?,?,?)",
                (identifier, title, time.time(), job.design.model_dump_json()),
            )
        return identifier


def templates():
    """List brand presets without returning their media paths."""
    with LOCK, database() as connection:
        return [
            {**dict(row), "bytes": item_bytes("templates", row["id"])}
            for row in connection.execute(
                "SELECT id,title,updated FROM templates WHERE deleted_at IS NULL ORDER BY updated DESC"
            )
        ]


def apply_template(job, identifier, store):
    """Reuse a brand template, retaining this episode's title and transcription content."""
    with LOCK, database() as connection:
        row = connection.execute(
            "SELECT * FROM templates WHERE id=? AND deleted_at IS NULL", (identifier,)
        ).fetchone()
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


def location(kind, identifier, trashed=False):
    """Read a managed UUID location without creating missing project/template directories."""
    if (
        kind not in ("projects", "templates")
        or len(identifier) != 32
        or any(c not in "0123456789abcdef" for c in identifier)
    ):
        raise HTTPException(404, "Saved item not found.")
    base = root()
    target = base / ("trash" if trashed else "") / kind / identifier
    if not target.resolve().is_relative_to(base.resolve()):
        raise ValueError("Saved item is outside the managed library.")
    for path in (target, target.parent, target.parent.parent):
        if path.is_symlink() or path.is_junction():
            raise ValueError("Library locations cannot be links or junctions.")
    return target


def item_bytes(kind, identifier, trashed=False):
    """Count actual local media bytes, including obsolete outputs retained in that item folder."""
    path = location(kind, identifier, trashed)
    return (
        sum(item.stat().st_size for item in path.iterdir() if item.is_file() and not item.is_symlink())
        if path.is_dir()
        else 0
    )


def rename(kind, identifier, title):
    """Rename a library label independently of the video's title and saved appearance."""
    if kind not in ("projects", "templates"):
        raise HTTPException(404, "Saved item not found.")
    with LOCK, database() as connection:
        column = "display_name" if kind == "projects" else "title"
        result = connection.execute(
            f"UPDATE {kind} SET {column}=?,updated=? WHERE id=? AND deleted_at IS NULL",
            (title.strip(), time.time(), identifier),
        )
        if not result.rowcount:
            raise HTTPException(404, "Saved item not found.")


def trash_item(kind, identifier):
    """Move a saved item into recoverable Trash; roll the move back if metadata cannot commit."""
    with LOCK, database() as connection:
        row = (
            connection.execute(
                f"SELECT * FROM {kind} WHERE id=? AND deleted_at IS NULL", (identifier,)
            ).fetchone()
            if kind in ("projects", "templates")
            else None
        )
        if not row:
            raise HTTPException(404, "Saved item not found.")
        source = location(kind, identifier)
        target = location(kind, identifier, True)
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        if target.exists():
            raise ValueError("Trash destination already exists.")
        source.replace(target)
        try:
            connection.execute(f"UPDATE {kind} SET deleted_at=? WHERE id=?", (time.time(), identifier))
            connection.commit()
        except BaseException:
            target.replace(source)
            raise


def trash_items():
    """List recoverable items with their space usage; no credentials or disk paths are returned."""
    with LOCK, database() as connection:
        result = []
        for kind in ("projects", "templates"):
            title = "COALESCE(display_name,title)" if kind == "projects" else "title"
            for row in connection.execute(
                f"SELECT id,{title} AS title,deleted_at FROM {kind} WHERE deleted_at IS NOT NULL ORDER BY deleted_at DESC"
            ):
                result.append(
                    {
                        **dict(row),
                        "confirm_name": row["title"] or row["id"],
                        "kind": kind,
                        "bytes": item_bytes(kind, row["id"], True),
                    }
                )
        return result


def restore_trash(kind, identifier):
    """Restore a Trash item to its original identity, preserving its drafts and saved settings."""
    if kind not in ("projects", "templates"):
        raise HTTPException(404, "Saved item not found.")
    with LOCK, database() as connection:
        row = connection.execute(
            f"SELECT id FROM {kind} WHERE id=? AND deleted_at IS NOT NULL", (identifier,)
        ).fetchone()
        if not row:
            raise HTTPException(404, "Trash item not found.")
        source = location(kind, identifier, True)
        target = location(kind, identifier)
        target.parent.mkdir(exist_ok=True, mode=0o700)
        if target.exists():
            raise ValueError("Restore destination already exists.")
        source.replace(target)
        try:
            connection.execute(f"UPDATE {kind} SET deleted_at=NULL WHERE id=?", (identifier,))
            connection.commit()
        except BaseException:
            target.replace(source)
            raise


def purge_trash(kind, identifier, confirmation):
    """Permanently remove only a named, already-trashed UUID item after explicit user confirmation."""
    if kind not in ("projects", "templates"):
        raise HTTPException(404, "Saved item not found.")
    with LOCK, database() as connection:
        expression = "COALESCE(display_name,title)" if kind == "projects" else "title"
        row = connection.execute(
            f"SELECT {expression} AS title FROM {kind} WHERE id=? AND deleted_at IS NOT NULL", (identifier,)
        ).fetchone()
        if not row:
            raise HTTPException(404, "Trash item not found.")
        if confirmation != (row["title"] or identifier):
            raise ValueError("Type the exact item name to permanently delete it.")
        target = location(kind, identifier, True)
        if target.is_dir():
            shutil.rmtree(target)
        connection.execute(f"DELETE FROM {kind} WHERE id=?", (identifier,))


def usage():
    """Report active and Trash bytes separately so deletion does not falsely promise freed space."""
    with LOCK:
        projects_size = sum(item["bytes"] for item in projects())
        templates_size = sum(item["bytes"] for item in templates())
        trash_size = sum(item["bytes"] for item in trash_items())
        path = root() / "library.sqlite3"
        database_size = path.stat().st_size if path.exists() else 0
        return {
            "projects_bytes": projects_size,
            "templates_bytes": templates_size,
            "trash_bytes": trash_size,
            "database_bytes": database_size,
            "total_bytes": projects_size + templates_size + trash_size + database_size,
            "free_bytes": shutil.disk_usage(root()).free,
        }


def srt_digest(text):
    """Hash normalized UTF-8 subtitle text for optimistic edit/autosave conflict detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def caption_state(job):
    """Read original caption text plus its recovery draft without applying unapproved corrections."""
    name = "generated.srt" if job.subtitle_source == "generate" else "original.srt"
    text = (job.path / name).read_text(encoding="utf-8-sig")
    result = {
        "srt": text,
        "base_digest": srt_digest(text),
        "base_version": 0,
        "draft": None,
        "draft_conflict": False,
    }
    if job.project_id:
        try:
            record = project(job.project_id)
        except HTTPException as exc:
            if exc.status_code == 404 and job.archive_error:
                return result  # The live SRT remains readable after a failed first archive.
            raise
        result["base_version"] = record["subtitle_version"]
        if record["subtitle_draft"]:
            draft = json.loads(record["subtitle_draft"])
            result["draft"] = draft["srt"]
            result["draft_conflict"] = (
                draft["base_digest"] != result["base_digest"]
                or draft["base_version"] != result["base_version"]
            )
    return result


def save_caption_draft(identifier, srt, base_digest, base_version):
    """Keep even incomplete SRT text, while rejecting obsolete saves from another edit generation."""
    if len(srt.encode("utf-8")) > settings.max_srt_bytes:
        raise ValueError("Subtitle draft exceeds the configured limit.")
    with LOCK, database() as connection:
        row = project(identifier)
        snapshot = json.loads(row["snapshot"])
        name = "generated.srt" if snapshot["subtitle_source"] == "generate" else "original.srt"
        original = (location("projects", identifier) / name).read_text(encoding="utf-8-sig")
        if base_digest != srt_digest(original) or base_version != row["subtitle_version"]:
            return False
        draft = json.dumps({"srt": srt, "base_digest": base_digest, "base_version": base_version})
        connection.execute(
            "UPDATE projects SET subtitle_draft=?,updated=? WHERE id=?", (draft, time.time(), identifier)
        )
        return True


def clear_caption_draft(identifier):
    """Advance the caption edit generation so late requests cannot resurrect saved/discarded drafts."""
    with LOCK, database() as connection:
        connection.execute(
            "UPDATE projects SET subtitle_draft=NULL,subtitle_version=subtitle_version+1 WHERE id=? AND deleted_at IS NULL",
            (identifier,),
        )
