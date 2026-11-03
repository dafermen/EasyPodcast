import time

from app.config import Settings
from app.jobs import store
from conftest import create


def test_default_retention_is_one_day():
    settings = Settings(_env_file=None)
    assert settings.ttl_seconds == 86400
    assert settings.active_ttl_seconds == 14400
    assert settings.failure_ttl_seconds == 900


def test_cookie_tracks_deadline_without_polling_extension(client, audio):
    data, headers = create(client, audio)
    job = store.jobs[data["id"]]
    job.expires = time.time() + 86400
    deadline = job.expires
    response = client.get("/api/jobs/" + data["id"], headers=headers)
    assert response.status_code == 200
    assert (
        "Max-Age=86399" in response.headers["set-cookie"] or "Max-Age=86400" in response.headers["set-cookie"]
    )
    assert job.expires == deadline
    job.expires = time.time() - 1
    assert client.get("/api/jobs/" + data["id"], headers=headers).status_code == 410
    store.cleanup()
    missing = client.get("/api/jobs/" + data["id"], headers=headers)
    assert missing.status_code == 404 and "reiniciar" in missing.json()["detail"]


def test_retention_is_exposed_without_secrets(client):
    retention = client.get("/api/capabilities").json()["retention"]
    assert retention["completed_seconds"] == 86400
    assert retention["survives_restart"] is False
