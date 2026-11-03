"""Durability, authorization, template and multi-format integration checks with synthetic media."""

from io import BytesIO

import pytest
from app import library
from app.config import settings
from app.jobs import store
from app.media import probe
from app.models import Design
from conftest import create
from PIL import Image
from test_api import wait


def session(client):
    """Establish the origin-protected library cookie used by the local browser."""
    response = client.post("/api/library/session")
    assert response.status_code == 200
    assert "HttpOnly" in response.headers["set-cookie"]


def test_durable_project_survives_restart_and_restores_draft(client, audio):
    data, headers = create(client, audio)
    identifier = data["project_id"]
    assert identifier and data["archive_error"] is None
    assert client.get("/api/projects").status_code == 401
    assert client.post("/api/library/session", headers={"Origin": "https://evil.example"}).status_code == 403
    session(client)
    draft = {**data["config"], "title": "Recovered draft"}
    assert (
        client.put(
            f"/api/projects/{identifier}/draft", json={"design": draft, "base": data["config"]}
        ).status_code
        == 200
    )
    assert client.get("/api/projects").json()[0]["has_draft"]
    original_token = data["token"]
    store.close()
    store.jobs.clear()
    store.stop.clear()
    store.start()
    reopened = client.post(f"/api/projects/{identifier}/open")
    assert reopened.status_code == 200, reopened.text
    job = reopened.json()
    assert job["config"]["title"] == "Recovered draft"
    assert job["token"] != original_token and job["project_id"] == identifier
    assert (store.jobs[job["id"]].path / "audio.bin").read_bytes() == audio
    assert client.get(f"/api/jobs/{job['id']}/artifacts/audio").status_code == 200
    listing = client.get("/api/projects").text
    assert (
        original_token not in listing and "token" not in listing and str(settings.library_root) not in listing
    )
    with library.database() as database:
        snapshot = database.execute("SELECT snapshot FROM projects WHERE id=?", (identifier,)).fetchone()[0]
    assert original_token not in snapshot
    duplicate = client.post(f"/api/projects/{identifier}/duplicate").json()
    assert duplicate["project_id"] != identifier and duplicate["config"]["title"].endswith("(copy)")


def test_stale_draft_does_not_replace_explicit_save(client, audio):
    data, headers = create(client, audio)
    session(client)
    saved = {**data["config"], "title": "Explicit saved design"}
    assert client.patch(f"/api/jobs/{data['id']}/config", headers=headers, json=saved).status_code == 200
    old = {**data["config"], "title": "Obsolete request"}
    client.put(f"/api/projects/{data['project_id']}/draft", json={"design": old, "base": data["config"]})
    opened = client.post(f"/api/projects/{data['project_id']}/open").json()
    assert opened["config"]["title"] == "Explicit saved design"


def test_templates_preserve_episode_content_and_copy_brand_media(client, audio):
    first, headers = create(client, audio)
    session(client)
    custom = {**first["config"], "title": "Brand preset", "title_font": "outfit", "subtitle_color": "#FFCC00"}
    client.patch(f"/api/jobs/{first['id']}/config", headers=headers, json=custom).raise_for_status()
    template = client.post(
        f"/api/jobs/{first['id']}/templates", headers=headers, json={"title": "Daily English"}
    ).json()["id"]
    folder = library.directory("templates", template)
    assert (folder / "background.png").exists() and not (folder / "audio.bin").exists()
    second, second_headers = create(client, audio)
    client.patch(
        f"/api/jobs/{second['id']}/config",
        headers=second_headers,
        json={**second["config"], "title": "New topic"},
    ).raise_for_status()
    result = client.post(f"/api/jobs/{second['id']}/templates/{template}", headers=second_headers)
    assert result.status_code == 200, result.text
    job = result.json()
    assert job["config"]["title"] == "New topic" and job["config"]["title_font"] == "outfit"
    assert not job["background_approved"] and not job["preview_approved"]
    assert client.get("/api/templates").json()[0]["title"] == "Daily English"
    assert client.post(
        f"/api/jobs/{second['id']}/templates/../../bad", headers=second_headers
    ).status_code in (404, 405)


@pytest.mark.parametrize(
    "format,size", [("landscape", (1920, 1080)), ("portrait", (1080, 1920)), ("square", (1080, 1080))]
)
def test_real_output_formats(client, audio, format, size):
    data, headers = create(client, audio, srt="1\n00:00:00,000 --> 00:00:01,000\nClear English")
    url = "/api/jobs/" + data["id"]
    design = Design(title="Clear English", output_format=format, preset="ultrafast")
    client.patch(url + "/config", headers=headers, json=design.model_dump()).raise_for_status()
    report = client.get(url + "/preflight", headers=headers).json()
    assert report["ready"] and (report["width"], report["height"]) == size
    client.post(url + "/background/approve", headers=headers).raise_for_status()
    client.post(url + "/preview", headers=headers, json={"start": 4}).raise_for_status()
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    metadata = probe(store.jobs[data["id"]].path / "preview.mp4")
    video = next(s for s in metadata["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == size
    assert client.get(url + "/artifacts/subtitles", headers=headers).status_code == 200


def test_preflight_detects_dense_text_and_logo_overlap(client, audio):
    logo = BytesIO()
    Image.new("RGBA", (100, 100), "red").save(logo, "PNG")
    response = client.post(
        "/api/jobs",
        files={
            "audio": ("audio.wav", audio),
            "srt": ("sub.srt", b"1\n00:00:00,000 --> 00:00:01,000\nHello"),
            "logo": ("logo.png", logo.getvalue(), "image/png"),
        },
    )
    data = response.json()
    headers = {"X-Job-Token": data["token"]}
    url = "/api/jobs/" + data["id"]
    design = Design(title="Hello", logo_x=0.47, logo_y=0.08, logo_scale=1.2)
    client.patch(url + "/config", headers=headers, json=design.model_dump()).raise_for_status()
    report = client.get(url + "/preflight", headers=headers).json()
    assert any("title" in warning for warning in report["warnings"])
    client.patch(
        url + "/config",
        headers=headers,
        json={**design.model_dump(), "output_format": "portrait", "title_offset_x": 600},
    ).raise_for_status()
    report = client.get(url + "/preflight", headers=headers).json()
    assert not report["ready"] and report["blockers"]
    client.post(url + "/background/approve", headers=headers)
    assert client.post(url + "/preview", headers=headers, json={"start": 0}).status_code == 409


def test_custom_logo_scale_and_position_in_portrait_render(client, audio, tmp_path):
    logo = BytesIO()
    Image.new("RGBA", (100, 100), (255, 0, 255, 255)).save(logo, "PNG")
    response = client.post(
        "/api/jobs",
        files={
            "audio": ("a.wav", audio),
            "srt": ("a.srt", b"1\n00:00:00,000 --> 00:00:01,000\nHello"),
            "logo": ("logo.png", logo.getvalue(), "image/png"),
        },
    )
    data = response.json()
    headers = {"X-Job-Token": data["token"]}
    url = "/api/jobs/" + data["id"]
    design = Design(
        output_format="portrait", title="Hello", logo_x=0.1, logo_y=0.2, logo_scale=1.2, preset="ultrafast"
    )
    client.patch(url + "/config", headers=headers, json=design.model_dump()).raise_for_status()
    client.post(url + "/background/approve", headers=headers).raise_for_status()
    client.post(url + "/preview", headers=headers, json={"start": 4}).raise_for_status()
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    image = tmp_path / "frame.png"
    import subprocess

    subprocess.run(
        [
            settings.ffmpeg,
            "-v",
            "error",
            "-i",
            str(store.jobs[data["id"]].path / "preview.mp4"),
            "-frames:v",
            "1",
            str(image),
        ],
        check=True,
    )
    with Image.open(image) as frame:
        red, green, blue = frame.convert("RGB").getpixel((168, 444))
        assert red > 180 and green < 70 and blue > 180


def test_portrait_background_is_preserved_and_templates_reuse_it(client, audio):
    image = BytesIO()
    Image.new("RGB", (600, 1000), (0, 128, 255)).save(image, "PNG")
    response = client.post(
        "/api/jobs",
        files={
            "audio": ("a.wav", audio),
            "srt": ("a.srt", b"1\n00:00:00,000 --> 00:00:01,000\nHello"),
            "image": ("portrait.png", image.getvalue(), "image/png"),
        },
    )
    assert response.status_code == 201, response.text
    job = response.json()
    source = store.jobs[job["id"]].path / "background-source.png"
    with Image.open(source) as saved:
        assert saved.size == (600, 1000)
    headers = {"X-Job-Token": job["token"]}
    session(client)
    template = client.post(f"/api/jobs/{job['id']}/templates", headers=headers).json()["id"]
    assert (library.directory("templates", template) / "background-source.png").exists()
    returned = client.get(f"/api/jobs/{job['id']}/artifacts/background", headers=headers)
    with Image.open(BytesIO(returned.content)) as downloaded:
        assert downloaded.size == (600, 1000)


def test_unknown_project_does_not_evict_and_archived_sessions_can_rotate(client, audio, monkeypatch):
    data, headers = create(client, audio)
    session(client)
    monkeypatch.setattr(settings, "max_jobs", 1)
    assert client.post("/api/projects/" + "0" * 32 + "/open").status_code == 404
    assert data["id"] in store.jobs
    duplicate = client.post(f"/api/projects/{data['project_id']}/duplicate")
    assert duplicate.status_code == 200, duplicate.text
    assert len(store.jobs) == 1 and data["id"] not in store.jobs
    reopened = client.post(f"/api/projects/{data['project_id']}/open")
    assert reopened.status_code == 200, reopened.text
    assert reopened.json()["project_id"] == data["project_id"]


def test_close_preserves_only_working_copy_when_archive_write_fails(client, audio, monkeypatch):
    data, headers = create(client, audio)

    def fail(job):
        raise OSError("simulated disk error")

    monkeypatch.setattr(library, "checkpoint", fail)
    response = client.delete(f"/api/jobs/{data['id']}", headers=headers)
    assert response.status_code == 507
    assert (store.jobs[data["id"]].path / "audio.bin").exists()


def test_reopen_running_job_restores_monitoring_without_restarting_it(client, audio):
    import time

    data, headers = create(client, audio)
    session(client)
    live = store.jobs[data["id"]]
    live.state = "rendering_video"
    live.progress = 0.4
    live.active_deadline = time.time() + 60
    response = client.post(f"/api/projects/{data['project_id']}/open")
    assert response.status_code == 200, response.text
    restored = response.json()
    assert restored["id"] == data["id"] and restored["state"] == "rendering_video"
    assert restored["progress"] == 0.4
    assert len(store.jobs) == 1


def test_preflight_is_read_only_during_media_downloads(client, audio):
    data, headers = create(client, audio)
    store.jobs[data["id"]].readers = 1
    try:
        result = client.get(f"/api/jobs/{data['id']}/preflight", headers=headers)
        assert result.status_code == 200, result.text
    finally:
        store.jobs[data["id"]].readers = 0
