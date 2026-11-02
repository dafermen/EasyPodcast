import threading
import time

import pytest
from app.config import settings
from app.jobs import Store, store
from app.models import Design
from app.subtitles import wrap_caption
from conftest import create
from test_api import wait


def test_cancel_running_process_releases_worker(client, audio):
    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    client.post(url + "/background/approve", headers=headers)
    client.post(url + "/preview", headers=headers, json={"start": 0})
    job = store.jobs[data["id"]]
    deadline = time.time() + 10
    while job.process is None and time.time() < deadline:
        time.sleep(0.01)
    process = job.process
    assert process is not None
    client.post(url + "/cancel", headers=headers)
    assert wait(client, url, headers)["state"] == "cancelled"
    assert process.poll() is not None and job.process is None
    assert not list(job.path.glob("*.partial.mp4"))
    client.post(url + "/preview", headers=headers, json={"start": 4.5})
    assert wait(client, url, headers)["state"] == "completed"


def test_queue_is_bounded(client, audio, monkeypatch):
    entered = threading.Event()
    release = threading.Event()

    class BlockingProvider:
        def generate_background(self, design, destination):
            entered.set()
            release.wait(10)
            raise ValueError("Proveedor bloqueado solo en prueba")

    monkeypatch.setattr(store, "provider", BlockingProvider())
    monkeypatch.setattr(settings, "openai_api_key", "fake-only")
    monkeypatch.setattr(settings, "image_model", "fake-only")
    jobs = [create(client, audio) for _ in range(4)]
    try:
        first, h = jobs[0]
        client.post("/api/jobs/" + first["id"] + "/background", headers=h)
        assert entered.wait(5)
        for data, headers in jobs[1:3]:
            assert client.post("/api/jobs/" + data["id"] + "/background", headers=headers).status_code == 200
        data, headers = jobs[3]
        response = client.post("/api/jobs/" + data["id"] + "/background", headers=headers)
        assert response.status_code == 422 and "cola" in response.json()["detail"]
    finally:
        release.set()
        for data, headers in jobs[:3]:
            wait(client, "/api/jobs/" + data["id"], headers)


def test_restart_cleans_only_managed_uuid(tmp_path, monkeypatch):
    root = tmp_path / "managed"
    root.mkdir()
    (root / ".easypodcast-root").touch()
    stale = root / ("a" * 32)
    stale.mkdir()
    (stale / "file").write_text("stale")
    reference = root / "keep-reference"
    reference.mkdir()
    monkeypatch.setattr(settings, "temp_root", root)
    instance = Store()
    instance.start()
    try:
        assert not stale.exists() and reference.exists()
    finally:
        instance.close()


def test_dense_subtitles_fail_without_truncation():
    with pytest.raises(ValueError, match="líneas"):
        wrap_caption("texto largo " * 100, Design())
