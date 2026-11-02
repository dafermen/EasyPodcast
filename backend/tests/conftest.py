import shutil
import subprocess

import pytest
from app.config import settings
from app.jobs import store
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "root", tmp_path / "jobs")
    monkeypatch.setattr(settings, "temp_root", tmp_path / "jobs")
    monkeypatch.setattr(settings, "min_free_bytes", 0)
    store.jobs.clear()
    store.stop.clear()
    with TestClient(
        app, base_url="http://127.0.0.1:8000", headers={"Origin": "http://127.0.0.1:8000"}
    ) as client:
        yield client


@pytest.fixture(scope="session")
def audio(tmp_path_factory):
    if not shutil.which(settings.ffmpeg) or not shutil.which(settings.ffprobe):
        pytest.skip("FFmpeg/FFprobe nativos requeridos")
    path = tmp_path_factory.mktemp("media") / "tone.wav"
    subprocess.run(
        [
            settings.ffmpeg,
            "-v",
            "error",
            "-f",
            "lavfi",
            "-i",
            r"aevalsrc=if(lt(mod(t\,2)\,1)\,0\,0.35*sin(2*PI*440*t)):s=44100:d=5",
            str(path),
        ],
        check=True,
    )
    return path.read_bytes()


SRT = "1\n00:00:00,500 --> 00:00:02,000\n¿Hola? Acentos: canción.\n\n2\n00:00:02,500 --> 00:00:04,500\nLlaves {texto} y barra \\N literal."


def create(client, audio, srt=SRT, filename="../../unsafe.wav"):
    response = client.post(
        "/api/jobs",
        files={"audio": (filename, audio, "audio/wav"), "srt": ("episode.srt", srt.encode(), "text/plain")},
    )
    assert response.status_code == 201, response.text
    data = response.json()
    return data, {"X-Job-Token": data["token"]}
