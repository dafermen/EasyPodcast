import pytest
from app.jobs import store
from app.models import Design
from app.subtitles import Word, clip_cues, make_ass, render_srt
from app.transcription import transcript_cues
from pydantic import ValidationError
from test_api import wait

WORDS = {
    "words": [
        {"start": 0.1, "end": 0.5, "text": "Build"},
        {"start": 0.6, "end": 1, "text": "clear"},
        {"start": 1.1, "end": 1.6, "text": "sentences."},
    ]
}


def test_word_timing_and_preview_offset():
    cues = transcript_cues(WORDS, 5)
    clipped = clip_cues(cues, 0.55, 1)
    assert clipped[0].word_offset == 5
    assert clipped[0].words[0].text == "clear"
    script = make_ass(clipped, Design(title=""), 1)
    assert r"Build {\c&H4AD5FF&}clear" in script
    assert "0:00:00.05,0:00:00.45" in script
    assert "\\N" not in render_srt(cues)


@pytest.mark.parametrize(
    "word",
    [
        {"start": -1, "end": 2, "text": "x"},
        {"start": 0, "end": float("nan"), "text": "x"},
        {"start": 1, "end": 1, "text": "x"},
    ],
)
def test_invalid_word_times(word):
    with pytest.raises(ValidationError):
        Word(**word)


def test_invalid_transcript_order_and_duration():
    with pytest.raises(ValueError):
        transcript_cues({"words": []}, 5)
    with pytest.raises(ValueError):
        transcript_cues(WORDS, 0.4)


def test_generated_job_review_download_edit(client, audio, monkeypatch):
    monkeypatch.setattr("app.transcription.available", lambda: True)

    def fake(job):
        cues = transcript_cues(WORDS, job.meta["duration"])
        return cues, render_srt(cues)

    monkeypatch.setattr("app.transcription.transcribe", fake)
    response = client.post(
        "/api/jobs?subtitle_mode=generate&language=en&model=tiny", files={"audio": ("demo.wav", audio)}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    headers = {"X-Job-Token": data["token"]}
    url = "/api/jobs/" + data["id"]
    result = wait(client, url, headers)
    assert result["state"] == "completed" and result["word_timestamps"] and not result["subtitles_approved"]
    assert client.post(url + "/preview", headers=headers, json={"start": 0}).status_code == 409
    assert client.get(url + "/subtitles").status_code == 404
    assert "Build clear sentences." in client.get(url + "/artifacts/subtitles", headers=headers).text
    assert client.post(url + "/subtitles/approve", headers=headers).json()["subtitles_approved"]
    original = client.get(url + "/subtitles", headers=headers).json()["srt"]
    store.jobs[data["id"]].readers = 1
    try:
        assert client.get(url + "/subtitles", headers=headers).status_code == 200
    finally:
        store.jobs[data["id"]].readers = 0
    unchanged = client.put(url + "/subtitles", headers=headers, json={"srt": original}).json()
    assert unchanged["word_timestamps"]
    updated = client.put(
        url + "/subtitles", headers=headers, json={"srt": original.replace("Build", "Make")}
    ).json()
    assert not updated["word_timestamps"] and not updated["subtitles_approved"]
    assert client.post(url + "/subtitles/approve", headers=headers).status_code == 200


def test_missing_srt_and_invalid_modes(client, audio, monkeypatch):
    assert client.post("/api/jobs", files={"audio": ("demo.wav", audio)}).status_code == 422
    assert (
        client.post("/api/jobs?subtitle_mode=evil", files={"audio": ("demo.wav", audio)}).status_code == 422
    )
    monkeypatch.setattr("app.transcription.available", lambda: False)
    assert (
        client.post("/api/jobs?subtitle_mode=generate", files={"audio": ("demo.wav", audio)}).status_code
        == 409
    )


def test_cancel_transcription_and_retry(client, audio, monkeypatch):
    monkeypatch.setattr("app.transcription.available", lambda: True)

    def fake(job):
        while not job.cancel.wait(0.01):
            pass
        raise InterruptedError()

    monkeypatch.setattr("app.transcription.transcribe", fake)
    r = client.post("/api/jobs?subtitle_mode=generate", files={"audio": ("demo.wav", audio)}).json()
    headers = {"X-Job-Token": r["token"]}
    url = "/api/jobs/" + r["id"]
    client.post(url + "/cancel", headers=headers)
    assert wait(client, url, headers)["state"] == "cancelled"

    def completed(job):
        cues = transcript_cues(WORDS, 5)
        return cues, render_srt(cues)

    monkeypatch.setattr("app.transcription.transcribe", completed)
    assert client.post(url + "/transcribe", headers=headers).status_code == 200
    assert wait(client, url, headers)["state"] == "completed"


def test_ffmpeg_highlights_only_current_word(client, audio, tmp_path):
    import subprocess

    from app.config import settings
    from conftest import create
    from PIL import Image

    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    design = Design(title="", font_size=64, preset="ultrafast")
    client.patch(url + "/config", headers=headers, json=design.model_dump())
    from app.subtitles import Cue

    store.jobs[data["id"]].cues = [
        Cue(
            0,
            2,
            "Clear English",
            (Word(start=0, end=0.8, text="Clear"), Word(start=0.8, end=2, text="English")),
        )
    ]
    client.post(url + "/background/approve", headers=headers)
    assert client.post(url + "/preview", headers=headers, json={"start": 0}).status_code == 200
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    video = store.jobs[data["id"]].path / "preview.mp4"
    centers = []
    for i, second in enumerate((0.4, 1.2)):
        image = tmp_path / f"word-{i}.png"
        subprocess.run(
            [
                settings.ffmpeg,
                "-v",
                "error",
                "-ss",
                str(second),
                "-i",
                str(video),
                "-frames:v",
                "1",
                str(image),
            ],
            check=True,
        )
        with Image.open(image) as frame:
            pixels = frame.convert("RGB")
            points = [
                x
                for y in range(850, 1030)
                for x in range(200, 1720)
                if (lambda c: c[0] > 180 and c[1] > 140 and c[2] < 130)(pixels.getpixel((x, y)))
            ]
            assert len(points) > 100
            centers.append(sum(points) / len(points))
    assert centers[1] - centers[0] > 40
