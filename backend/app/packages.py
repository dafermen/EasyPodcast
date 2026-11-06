"""Portable, checksummed ZIP packages without database credentials or unsafe extraction paths."""

import copy
import hashlib
import json
import math
import os
import shutil
import stat
import subprocess
import time
import uuid
import zipfile
from pathlib import PurePosixPath

from PIL import Image

from . import library
from .config import settings
from .media import normalize_image, probe, validate_audio
from .models import Design, SubtitleDraftRequest, TranscriptionOptions
from .subtitles import Word, parse_srt

MAX_MANIFEST = 64 * 1024**2
MAX_MEMBERS = 10000
TEMPLATE_FILES = {"background.png", "background-source.png", "logo.png"}


def digest(path):
    """Hash a file in fixed-size chunks so large audio/video never becomes an in-memory Blob."""
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024**2), b""):
            value.update(block)
    return value.hexdigest()


def records(scope, identifier=None):
    """Snapshot records under the library lock; private owner keys and SQLite files are excluded."""
    with library.database() as connection:
        if scope == "project":
            return [("projects", library.project(identifier))]
        if scope != "library":
            raise ValueError("Unsupported package scope.")
        return [
            (kind, dict(row))
            for kind in ("projects", "templates")
            for row in connection.execute(f"SELECT * FROM {kind}")
        ]


def build(stage, scope, identifier=None):
    """Freeze media versions using hard links when possible, then build a ZIP64 package on disk."""
    manifest = {
        "format": "easypodcast-portable",
        "version": 1,
        "scope": scope,
        "created": time.time(),
        "items": [],
    }
    frozen = stage / "frozen"
    frozen.mkdir()
    with library.LOCK:
        rows = records(scope, identifier)
        if len(rows) > 2000:
            raise ValueError("Too many items for one portable package.")
        file_count = 1  # The manifest itself is also a ZIP member.
        for kind, row in rows:
            record = copy.deepcopy(row)
            saved = json.loads(record["snapshot"]) if kind == "projects" else None
            names = set(saved["files"]) if saved else TEMPLATE_FILES
            if kind == "projects" and not names.issubset(library.FILES):
                raise ValueError("Saved project contains an unsupported media filename.")
            folder = library.location(kind, record["id"], record.get("deleted_at") is not None)
            entry = {"kind": kind, "record": record, "files": {}}
            for name in sorted(names):
                source = folder / name
                if not source.is_file():
                    if name in ("audio.bin", "background.png"):
                        raise ValueError("Required project input is missing; export was cancelled.")
                    continue
                if source.is_symlink():
                    raise ValueError("Library media cannot be a symbolic link.")
                target = frozen / kind / record["id"] / name
                target.parent.mkdir(parents=True, exist_ok=True)
                try:
                    os.link(source, target)
                except OSError:
                    library.copy_file(source, target)
                entry["files"][name] = {"size": target.stat().st_size, "sha256": None}
            file_count += len(entry["files"])
            if file_count > MAX_MEMBERS:
                raise ValueError("Too many media files for one portable package.")
            manifest["items"].append(entry)
    total = 0
    output = stage / "package.easypodcast.zip"
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
        for entry in manifest["items"]:
            for name, meta in entry["files"].items():
                source = frozen / entry["kind"] / entry["record"]["id"] / name
                total += source.stat().st_size
                if (
                    total > settings.max_bundle_bytes
                    or shutil.disk_usage(stage).free < source.stat().st_size + settings.min_free_bytes
                ):
                    raise ValueError("Package exceeds the configured size or available disk space.")
                meta["sha256"] = digest(source)
                archive.write(source, f"{entry['kind']}/{entry['record']['id']}/{name}")
        raw = json.dumps(manifest, ensure_ascii=False).encode("utf-8")
        if len(raw) > MAX_MANIFEST:
            raise ValueError("Package manifest is too large.")
        archive.writestr("manifest.json", raw)
    if output.stat().st_size > settings.max_bundle_bytes:
        raise ValueError("Package exceeds the configured size limit.")
    return output


def validate_project(record, folder, names):
    """Validate imported settings/media and rebuild trustworthy audio metadata before installation."""
    saved = json.loads(record["snapshot"])
    if not isinstance(saved, dict):
        raise ValueError("Invalid project snapshot.")
    if saved.get("schema_version", 1) != 1 or not {"audio.bin", "background.png"}.issubset(names):
        raise ValueError("Unsupported or incomplete saved project.")
    design = Design.model_validate(saved["config"])
    saved["config"] = design.model_dump()
    saved["metadata"] = validate_audio(folder / "audio.bin")
    source = saved.get("subtitle_source")
    if source not in ("upload", "generate"):
        raise ValueError("Unsupported subtitle source.")
    srt_name = "generated.srt" if source == "generate" else "original.srt"
    if srt_name in names:
        parsed, warnings = parse_srt((folder / srt_name).read_bytes())
        serialized = saved.get("cues", [])
        if (
            not isinstance(serialized, list)
            or len(serialized) > 100000
            or any(not isinstance(c, dict) for c in serialized)
        ):
            raise ValueError("Invalid subtitle cue metadata.")
        if len(serialized) != len(parsed):
            serialized = []
        cues = []
        word_count = 0
        for index, cue in enumerate(parsed):
            original = serialized[index] if serialized else {}
            words = []
            if (
                original.get("text") == cue.text
                and abs(original.get("start", -1) - cue.start) < 0.001
                and abs(original.get("end", -1) - cue.end) < 0.001
            ):
                for item in original.get("words", []):
                    word = Word.model_validate(item)
                    if (
                        word.start < cue.start - 0.001
                        or word.end > cue.end + 0.05
                        or (words and word.start < words[-1]["end"])
                    ):
                        raise ValueError("Imported word timing is invalid.")
                    words.append(word.model_dump())
                    word_count += 1
                    if word_count > 150000:
                        raise ValueError("Too many imported word timestamps.")
            cues.append(
                {"start": cue.start, "end": cue.end, "text": cue.text, "words": words, "word_offset": 0}
            )
        saved["cues"] = cues
        saved["warnings"] = warnings
    elif source == "upload" or saved.get("cues"):
        raise ValueError("Package is missing subtitle media.")
    else:
        saved["cues"] = []
        saved["warnings"] = []
    saved["transcription_options"] = TranscriptionOptions.model_validate(
        saved.get("transcription_options", {})
    ).model_dump()
    for key in ("background_approved", "preview_approved", "subtitles_approved"):
        if not isinstance(saved.get(key), bool):
            raise ValueError("Invalid saved approval state.")
    if saved.get("background_mode") not in ("local", "upload", "openai"):
        raise ValueError("Invalid background source.")
    artifacts = {"background"}
    if "logo.png" in names:
        artifacts.add("logo")
    if srt_name in names:
        artifacts.add("subtitles")
    for name in ("preview.mp4", "video.mp4"):
        if name not in names:
            continue
        try:
            media = probe(folder / name)
        except (OSError, subprocess.SubprocessError) as exc:
            raise ValueError("Imported video is not valid media.") from exc
        videos = [item for item in media.get("streams", []) if item["codec_type"] == "video"]
        audios = [item for item in media.get("streams", []) if item["codec_type"] == "audio"]
        if (
            not videos
            or not audios
            or videos[0]["codec_name"] != "h264"
            or audios[0]["codec_name"] != "aac"
            or (videos[0]["width"], videos[0]["height"]) != design.frame_size
        ):
            raise ValueError("Imported video does not match its saved format.")
        artifacts.add(name.removesuffix(".mp4"))
    if "preview" not in artifacts:
        saved["preview_approved"] = False
    saved["artifacts"] = sorted(artifacts)
    saved["files"] = {
        name: [(folder / name).stat().st_size, (folder / name).stat().st_mtime_ns] for name in names
    }
    record["snapshot"] = json.dumps(saved)
    if record.get("draft"):
        record["draft"] = Design.model_validate_json(record["draft"]).model_dump_json()
    draft = record.get("subtitle_draft")
    if draft:
        parsed = json.loads(draft)
        if not isinstance(parsed.get("srt"), str) or len(parsed["srt"].encode()) > settings.max_srt_bytes:
            raise ValueError("Invalid subtitle recovery draft.")
        if srt_name not in names:
            raise ValueError("Caption draft has no original subtitles.")
        record["subtitle_draft"] = SubtitleDraftRequest.model_validate(parsed).model_dump_json()


def inspect_package(stage):
    """Verify every ZIP name/hash/budget before creating any durable library record."""
    extracted = stage / "validated"
    extracted.mkdir()
    try:
        with zipfile.ZipFile(stage / "upload.zip") as archive:
            infos = archive.infolist()
            if len(infos) > MAX_MEMBERS or len({i.filename.casefold() for i in infos}) != len(infos):
                raise ValueError("Package contains duplicate names or too many entries.")
            for info in infos:
                path = PurePosixPath(info.filename)
                if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                    raise ValueError("Unsupported ZIP compression.")
                if (
                    info.is_dir()
                    or path.is_absolute()
                    or ".." in path.parts
                    or "\\" in info.filename
                    or ":" in info.filename
                    or info.flag_bits & 1
                    or stat.S_ISLNK(info.external_attr >> 16)
                ):
                    raise ValueError("Unsafe or unsupported ZIP entry.")
            if sum(i.file_size for i in infos) > settings.max_bundle_expanded_bytes:
                raise ValueError("Expanded package exceeds the configured limit.")
            info = archive.getinfo("manifest.json")
            if info.file_size > MAX_MANIFEST:
                raise ValueError("Package manifest is too large.")
            manifest = json.loads(archive.read(info))
            if not isinstance(manifest, dict):
                raise ValueError("Invalid package manifest.")
            if (
                manifest.get("format") != "easypodcast-portable"
                or manifest.get("version") != 1
                or manifest.get("scope") not in ("project", "library")
            ):
                raise ValueError("This is not a supported EasyPodcast package.")
            entries = manifest.get("items")
            if not isinstance(entries, list) or len(entries) > 2000:
                raise ValueError("Invalid package item list.")
            allowed = {"manifest.json"}
            identities = set()
            expanded = 0
            for entry in entries:
                if not isinstance(entry, dict) or not isinstance(entry.get("record"), dict):
                    raise ValueError("Invalid saved item record.")
                kind = entry["kind"]
                record = entry["record"]
                identifier = record["id"]
                if (
                    kind not in ("projects", "templates")
                    or not isinstance(identifier, str)
                    or len(identifier) != 32
                    or any(c not in "0123456789abcdef" for c in identifier)
                    or (kind, identifier) in identities
                ):
                    raise ValueError("Invalid or duplicate saved item identity.")
                identities.add((kind, identifier))
                if (
                    not isinstance(record.get("title"), str)
                    or len(record["title"]) > 120
                    or (
                        record.get("display_name") is not None
                        and (not isinstance(record["display_name"], str) or len(record["display_name"]) > 120)
                    )
                ):
                    raise ValueError("Invalid saved item name.")
                for key in ("created", "updated", "deleted_at"):
                    value = record.get(key)
                    if value is not None and (
                        type(value) not in (int, float) or not math.isfinite(value) or value < 0
                    ):
                        raise ValueError("Invalid saved timestamp.")
                version = record.get("subtitle_version", 0)
                if type(version) is not int or not 0 <= version < 2**53:
                    raise ValueError("Invalid subtitle draft version.")
                folder = extracted / kind / identifier
                folder.mkdir(parents=True)
                files = entry["files"]
                if not isinstance(files, dict) or not set(files).issubset(
                    library.FILES if kind == "projects" else TEMPLATE_FILES
                ):
                    raise ValueError("Package contains an unsupported media filename.")
                for name, meta in files.items():
                    if not isinstance(meta, dict):
                        raise ValueError("Invalid file metadata.")
                    member = f"{kind}/{identifier}/{name}"
                    allowed.add(member)
                    part = archive.getinfo(member)
                    if (
                        type(meta.get("size")) is not int
                        or part.file_size != meta["size"]
                        or not isinstance(meta.get("sha256"), str)
                        or len(meta["sha256"]) != 64
                    ):
                        raise ValueError("Invalid package checksum metadata.")
                    maximum = (
                        settings.max_audio_bytes
                        if name == "audio.bin"
                        else settings.max_image_bytes
                        if name.endswith(".png")
                        else settings.max_srt_bytes
                        if name.endswith(".srt")
                        else settings.max_bundle_expanded_bytes
                    )
                    if part.file_size > maximum:
                        raise ValueError("A packaged file exceeds its configured limit.")
                    value = hashlib.sha256()
                    written = 0
                    with archive.open(part) as source, (folder / name).open("xb") as target:
                        for block in iter(lambda: source.read(1024**2), b""):
                            written += len(block)
                            expanded += len(block)
                            if (
                                written > maximum
                                or expanded > settings.max_bundle_expanded_bytes
                                or shutil.disk_usage(stage).free < len(block) + settings.min_free_bytes
                            ):
                                raise ValueError("Package exceeds size or free-space limits.")
                            value.update(block)
                            target.write(block)
                    if written != meta["size"] or value.hexdigest() != meta["sha256"]:
                        raise ValueError("Package checksum verification failed.")
                    if name.endswith(".png"):
                        normalized = folder / "normalized.png"
                        normalize_image(
                            folder / name, normalized, name == "logo.png", name == "background-source.png"
                        )
                        normalized.replace(folder / name)
                if kind == "projects":
                    validate_project(record, folder, set(files))
                else:
                    if "background.png" not in files:
                        raise ValueError("Template background is missing.")
                    record["design"] = Design.model_validate_json(record["design"]).model_dump_json()
            if set(i.filename for i in infos) != allowed:
                raise ValueError("Package contains unexpected entries.")
            if manifest["scope"] == "project" and (len(entries) != 1 or entries[0]["kind"] != "projects"):
                raise ValueError("Invalid portable project contents.")
            (stage / "verified.json").write_text(json.dumps(manifest), encoding="utf-8")
            return {
                "scope": manifest["scope"],
                "items": [
                    {
                        "kind": e["kind"],
                        "title": e["record"].get("display_name") or e["record"]["title"],
                        "bytes": sum(f["size"] for f in e["files"].values()),
                        "in_trash": e["record"].get("deleted_at") is not None,
                    }
                    for e in entries
                ],
                "bytes": expanded,
            }
    except (
        AttributeError,
        OverflowError,
        KeyError,
        TypeError,
        UnicodeError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
        RuntimeError,
    ) as exc:
        raise ValueError("Invalid or damaged EasyPodcast package.") from exc


def install(stage):
    """Merge verified items under fresh IDs; roll back newly created copies on any installation failure."""
    manifest = json.loads((stage / "verified.json").read_text(encoding="utf-8"))
    created = []
    projects = []
    templates = []
    with library.LOCK:
        try:
            with library.database() as connection:
                for entry in manifest["items"]:
                    kind = entry["kind"]
                    record = entry["record"]
                    identifier = uuid.uuid4().hex
                    target = library.directory(kind, identifier)
                    created.append(target)
                    source = stage / "validated" / kind / record["id"]
                    for name in entry["files"]:
                        library.copy_file(source / name, target / name)
                    deleted = time.time() if record.get("deleted_at") is not None else None
                    if kind == "projects":
                        saved = json.loads(record["snapshot"])
                        saved["files"] = {
                            name: [(target / name).stat().st_size, (target / name).stat().st_mtime_ns]
                            for name in entry["files"]
                        }
                        connection.execute(
                            "INSERT INTO projects (id,title,created,updated,state,snapshot,draft,display_name,deleted_at,subtitle_draft,subtitle_version) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (
                                identifier,
                                record["title"],
                                time.time(),
                                time.time(),
                                "ready",
                                json.dumps(saved),
                                record.get("draft"),
                                record.get("display_name"),
                                deleted,
                                record.get("subtitle_draft"),
                                int(record.get("subtitle_version") or 0),
                            ),
                        )
                        with Image.open(target / "background.png") as image:
                            image.thumbnail((320, 180))
                            image.convert("RGB").save(target / "thumbnail.png")
                        projects.append(identifier)
                    else:
                        connection.execute(
                            "INSERT INTO templates (id,title,updated,design,deleted_at) VALUES (?,?,?,?,?)",
                            (identifier, record["title"], time.time(), record["design"], deleted),
                        )
                        templates.append(identifier)
                    if deleted:
                        destination = library.location(kind, identifier, True)
                        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
                        target.replace(destination)
                        created[-1] = destination
            return {"projects": projects, "templates": templates}
        except BaseException:
            for path in created:
                if (
                    path.resolve().is_relative_to(library.root().resolve())
                    and path.is_dir()
                    and not path.is_symlink()
                ):
                    shutil.rmtree(path)
            raise
