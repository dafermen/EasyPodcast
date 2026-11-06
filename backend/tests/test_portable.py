"""Portable-project, safe restore, Trash and raw subtitle recovery integration tests."""

import io
import json
import zipfile

import pytest
from app import library
from app.config import settings
from app.jobs import store
from conftest import create
from test_library import session


def export(client, path):
    """Build and consume a single-use disk-backed package download."""
    response = client.post(path)
    assert response.status_code == 200, response.text
    url = response.json()["url"]
    download = client.get(url)
    assert download.status_code == 200
    assert client.get(url).status_code == 404
    return download.content


def inspect(client, content):
    """Upload a raw ZIP and require successful validation before any installation."""
    response = client.post(
        "/api/library/import", content=content, headers={"Content-Type": "application/zip"}
    )
    assert response.status_code == 200, response.text
    return response.json()


def rewrite(content, change):
    """Create deliberately invalid package variants without touching the durable library."""
    source = zipfile.ZipFile(io.BytesIO(content))
    entries = {name: source.read(name) for name in source.namelist()}
    change(entries)
    target = io.BytesIO()
    with zipfile.ZipFile(target, "w") as archive:
        for name, value in entries.items():
            archive.writestr(name, value)
    return target.getvalue()


def test_project_roundtrip_is_reviewed_new_copy_and_preserves_drafts(client, audio):
    job, headers = create(client, audio)
    session(client)
    pid = job["project_id"]
    state = client.get(f"/api/jobs/{job['id']}/subtitles", headers=headers).json()
    draft = {
        "srt": "incomplete correction",
        "base_digest": state["base_digest"],
        "base_version": state["base_version"],
    }
    assert client.put(f"/api/projects/{pid}/subtitle-draft", json=draft).json()["saved"]
    client.put(
        f"/api/projects/{pid}/draft",
        json={"design": {**job["config"], "title": "Portable draft"}, "base": job["config"]},
    ).raise_for_status()
    client.patch(
        f"/api/library/items/projects/{pid}", json={"title": "My portable episode"}
    ).raise_for_status()
    content = export(client, f"/api/projects/{pid}/export")
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        names = archive.namelist()
        manifest = archive.read("manifest.json")
        assert all("owner" not in n and "sqlite" not in n for n in names)
        assert job["token"].encode() not in manifest
    review = inspect(client, content)
    assert len(client.get("/api/projects").json()) == 1
    imported = client.post(f"/api/library/imports/{review['ticket']}/confirm").json()["projects"][0]
    assert imported != pid
    assert client.post(f"/api/library/imports/{review['ticket']}/confirm").status_code == 404
    opened = client.post(f"/api/projects/{imported}/open").json()
    assert opened["config"]["title"] == "Portable draft"
    assert opened["subtitle_draft_available"]
    recovered = client.get(
        f"/api/jobs/{opened['id']}/subtitles", headers={"X-Job-Token": opened["token"]}
    ).json()
    assert recovered["draft"] == "incomplete correction" and not recovered["draft_conflict"]
    assert (store.jobs[opened["id"]].path / "audio.bin").read_bytes() == audio


def test_backup_restores_templates_and_trash_without_overwrite(client, audio):
    job, headers = create(client, audio)
    session(client)
    tid = client.post(f"/api/jobs/{job['id']}/templates", headers=headers, json={"title": "Brand"}).json()[
        "id"
    ]
    client.post(f"/api/library/items/templates/{tid}/trash").raise_for_status()
    content = export(client, "/api/library/backup")
    review = inspect(client, content)
    assert any(i["kind"] == "templates" and i["in_trash"] for i in review["items"])
    result = client.post(f"/api/library/imports/{review['ticket']}/confirm").json()
    assert len(result["projects"]) == len(result["templates"]) == 1
    assert len(client.get("/api/projects").json()) == 2
    assert len(client.get("/api/library/trash").json()) == 2
    copy = result["templates"][0]
    client.post(f"/api/library/trash/templates/{copy}/restore").raise_for_status()
    assert client.get("/api/templates").json()[0]["title"] == "Brand"


def test_trash_rename_restore_and_typed_purge_only_isolated_fixture(client, audio):
    job, headers = create(client, audio)
    session(client)
    pid = job["project_id"]
    client.patch(f"/api/library/items/projects/{pid}", json={"title": "Library label"}).raise_for_status()
    assert store.jobs[job["id"]].design.title == job["config"]["title"]
    size = client.get("/api/library/usage").json()["projects_bytes"]
    assert size > 0
    client.post(f"/api/library/items/projects/{pid}/trash").raise_for_status()
    assert client.get("/api/projects").json() == []
    assert client.get("/api/library/usage").json()["trash_bytes"] == size
    assert client.post(f"/api/projects/{pid}/open").status_code == 404
    client.post(f"/api/library/trash/projects/{pid}/restore").raise_for_status()
    assert client.get("/api/projects").json()[0]["title"] == "Library label"
    client.post(f"/api/library/items/projects/{pid}/trash").raise_for_status()
    assert (
        client.request(
            "DELETE", f"/api/library/trash/projects/{pid}", json={"confirmation": "wrong"}
        ).status_code
        == 422
    )
    client.request(
        "DELETE", f"/api/library/trash/projects/{pid}", json={"confirmation": "Library label"}
    ).raise_for_status()
    assert client.get("/api/library/trash").json() == []


@pytest.mark.parametrize("variant", ["traversal", "extra", "checksum", "malformed", "record", "duplicate"])
def test_invalid_import_never_changes_library(client, audio, variant):
    job, _ = create(client, audio)
    session(client)
    content = export(client, f"/api/projects/{job['project_id']}/export")

    def damage(entries):
        """Alter one security boundary per fixture."""
        if variant == "traversal":
            entries["../escape.txt"] = b"bad"
        elif variant == "extra":
            entries["extra.txt"] = b"bad"
        elif variant == "checksum":
            name = next(n for n in entries if n.endswith("audio.bin"))
            entries[name] = b"bad"
        elif variant == "duplicate":
            entries["MANIFEST.JSON"] = entries["manifest.json"]
        else:
            manifest = json.loads(entries["manifest.json"])
            if variant == "malformed":
                manifest = []
            else:
                manifest["items"][0]["record"]["display_name"] = {"bad": "shape"}
            entries["manifest.json"] = json.dumps(manifest).encode()

    result = client.post("/api/library/import", content=rewrite(content, damage))
    assert result.status_code == 422, result.text
    assert len(client.get("/api/projects").json()) == 1
    assert not list(store.root.glob("*/validated"))


def test_cancel_import_and_limits(client, audio, monkeypatch):
    job, _ = create(client, audio)
    session(client)
    content = export(client, f"/api/projects/{job['project_id']}/export")
    review = inspect(client, content)
    client.delete(f"/api/library/imports/{review['ticket']}").raise_for_status()
    assert client.post(f"/api/library/imports/{review['ticket']}/confirm").status_code == 404
    monkeypatch.setattr(settings, "max_bundle_bytes", 100)
    assert client.post("/api/library/import", content=content).status_code == 413
    assert len(client.get("/api/projects").json()) == 1


def test_raw_subtitle_recovery_generation_conflicts_and_render_gate(client, audio):
    job, headers = create(client, audio)
    session(client)
    pid = job["project_id"]
    jid = job["id"]
    state = client.get(f"/api/jobs/{jid}/subtitles", headers=headers).json()
    draft = {
        "srt": "incomplete text",
        "base_digest": state["base_digest"],
        "base_version": state["base_version"],
    }
    assert client.put(f"/api/projects/{pid}/subtitle-draft", json=draft).json()["saved"]
    assert client.post(f"/api/jobs/{jid}/preview", headers=headers, json={"start": 0}).status_code == 409
    assert client.post(f"/api/jobs/{jid}/subtitles/approve", headers=headers).status_code == 409
    reopened = client.post(f"/api/projects/{pid}/open").json()
    assert reopened["subtitle_draft_available"]
    client.delete(f"/api/projects/{pid}/subtitle-draft").raise_for_status()
    assert not client.put(f"/api/projects/{pid}/subtitle-draft", json=draft).json()["saved"]
    state = client.get(f"/api/jobs/{jid}/subtitles", headers=headers).json()
    corrected = state["srt"].replace("¿Hola?", "Hello!")
    body = {"srt": corrected, "base_digest": state["base_digest"], "base_version": state["base_version"]}
    client.put(f"/api/jobs/{jid}/subtitles", headers=headers, json=body).raise_for_status()
    assert client.put(f"/api/jobs/{jid}/subtitles", headers=headers, json=body).status_code == 409
    assert client.get(f"/api/jobs/{jid}/subtitles", headers=headers).json()["draft"] is None


def test_management_auth_and_active_job_guard(client, audio):
    job, _ = create(client, audio)
    assert client.get("/api/library/usage").status_code == 401
    session(client)
    assert client.post("/api/library/backup", headers={"Origin": "https://evil.example"}).status_code == 403
    store.jobs[job["id"]].state = "rendering_video"
    assert client.post(f"/api/library/items/projects/{job['project_id']}/trash").status_code == 409
    store.jobs[job["id"]].state = "ready"


def test_import_failure_rolls_back_new_files_and_records(client, audio, monkeypatch):
    """A failed installation leaves the existing project intact and no half-imported copy."""
    from app import packages

    job, _ = create(client, audio)
    session(client)
    review = inspect(client, export(client, f"/api/projects/{job['project_id']}/export"))
    from app.main import app

    entry = app.state.transfers.entries[review["ticket"]]
    original = library.copy_file
    calls = 0

    def fail(source, target):
        """Inject a controlled disk failure after one successful media copy."""
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated disk failure")
        return original(source, target)

    monkeypatch.setattr(library, "copy_file", fail)
    with pytest.raises(OSError):
        packages.install(entry["path"])
    assert len(library.projects()) == 1
    assert len(list((library.root() / "projects").iterdir())) == 1


def test_portable_generated_word_timing_survives(client, audio):
    """Revalidate generated word intervals while preserving current-word highlighting."""
    from app.subtitles import Cue, Word

    job, _ = create(client, audio)
    current = store.jobs[job["id"]]
    current.subtitle_source = "generate"
    current.cues = [
        Cue(
            0.5,
            2,
            "Clear English",
            (Word(start=0.5, end=1, text="Clear"), Word(start=1.1, end=2, text="English")),
        )
    ]
    (current.path / "generated.srt").write_text(
        "1\n00:00:00,500 --> 00:00:02,000\nClear English\n", encoding="utf-8"
    )
    store.checkpoint(current)
    session(client)
    review = inspect(client, export(client, f"/api/projects/{job['project_id']}/export"))
    identifier = client.post(f"/api/library/imports/{review['ticket']}/confirm").json()["projects"][0]
    opened = client.post(f"/api/projects/{identifier}/open").json()
    assert opened["word_timestamps"]
    assert store.jobs[opened["id"]].cues[0].words[0].text == "Clear"


def test_transfer_expiry_cannot_remove_busy_lease(client):
    """Expiry skips consumers holding a lease and removes their staging only after release."""
    from app.main import app

    manager = app.state.transfers
    entry = manager.begin("import")
    manager.ready(entry)
    with manager.lease(entry["id"], "import"):
        entry["expires"] = 0
        manager.clean()
        assert entry["path"].exists()
    manager.clean()
    assert not entry["path"].exists()


def test_export_obeys_import_member_budget(client, audio, monkeypatch):
    """Never produce a package that the same version would reject for too many members."""
    from app import packages

    job, _ = create(client, audio)
    session(client)
    monkeypatch.setattr(packages, "MAX_MEMBERS", 2)
    response = client.post(f"/api/projects/{job['project_id']}/export")
    assert response.status_code == 422
    assert len(library.projects()) == 1
