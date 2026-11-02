import time

import pytest
from app.config import settings
from app.jobs import ACTIVE, store
from app.media import local_background, normalize_image
from conftest import create
from PIL import Image


def test_security_validation_and_delete(client, audio):
    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    assert client.get(url).status_code == 404
    assert client.get(url, headers={"X-Job-Token": "wrong"}).status_code == 404
    assert client.get(url, headers=headers).status_code == 200
    assert (
        client.post(url + "/cancel", headers={**headers, "Origin": "https://evil.example"}).status_code == 403
    )
    assert client.get("/api/health", headers={"Host": "evil.example"}).status_code == 400
    assert client.patch(url + "/config", headers=headers, json={"color": "red;movie=evil"}).status_code == 422
    assert client.get(url + "/artifacts/unknown", headers=headers).status_code == 404
    response = client.get(url + "/artifacts/background", headers={"Range": "bytes=0-31"})
    assert response.status_code == 206 and len(response.content) == 32
    assert client.get(url + "/artifacts/config", headers=headers).json().get("title")
    job_path = store.jobs[data["id"]].path
    assert job_path.name == data["id"] and not (store.root / "unsafe.wav").exists()
    assert client.delete(url, headers=headers).status_code == 200
    assert not job_path.exists()


def test_fake_audio_empty_srt_and_size(client, audio, monkeypatch):
    r = client.post("/api/jobs", files={"audio": ("fake.wav", b"fake"), "srt": ("a.srt", b"bad")})
    assert r.status_code == 422
    r = client.post("/api/jobs", files={"audio": ("x.wav", audio), "srt": ("a.srt", b"")})
    assert r.status_code == 422
    monkeypatch.setattr(settings, "max_audio_bytes", 100)
    r = client.post("/api/jobs", files={"audio": ("x.wav", audio), "srt": ("a.srt", b"bad")})
    assert r.status_code == 413


def test_image_validation(tmp_path, monkeypatch):
    source = tmp_path / "image.png"
    Image.new("RGB", (100, 100)).save(source)
    monkeypatch.setattr(settings, "max_pixels", 50)
    with pytest.raises(ValueError):
        normalize_image(source, tmp_path / "out.png")
    source.write_text("<svg/>")
    with pytest.raises(ValueError):
        normalize_image(source, tmp_path / "out.png")


def test_expiration_waits_for_reader(client, audio):
    data, headers = create(client, audio)
    job = store.jobs[data["id"]]
    job.readers = 1
    job.expires = time.time() - 1
    store.cleanup()
    assert job.path.exists()
    job.readers = 0
    store.cleanup()
    assert not job.path.exists()
    assert client.get("/api/jobs/" + data["id"], headers=headers).status_code == 404


class FakeProvider:
    def generate_background(self, design, destination):
        local_background(destination)


def wait(client, url, headers, timeout=90):
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = client.get(url, headers=headers).json()
        if data["state"] not in ACTIVE:
            return data
        time.sleep(0.15)
    pytest.fail("Trabajo no terminó en el tiempo de prueba")


def test_fake_provider_and_error(client, audio, monkeypatch):
    monkeypatch.setattr(settings, "openai_api_key", "test-only")
    monkeypatch.setattr(settings, "image_model", "fake-test-only")
    monkeypatch.setattr(store, "provider", FakeProvider())
    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    assert client.post(url + "/background", headers=headers).status_code == 200
    result = wait(client, url, headers)
    assert result["state"] == "completed" and result["background_mode"] == "openai"
    assert result["background_approved"] is False

    class BrokenProvider:
        def generate_background(self, design, destination):
            raise ValueError("Cuota agotada (prueba simulada)")

    monkeypatch.setattr(store, "provider", BrokenProvider())
    client.post(url + "/background", headers=headers)
    result = wait(client, url, headers)
    assert result["state"] == "failed" and "simulada" in result["error"]
