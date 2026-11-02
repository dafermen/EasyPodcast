import subprocess
from array import array

import pytest
from app.config import settings
from app.jobs import store
from app.media import probe
from conftest import create
from PIL import Image, ImageChops, ImageStat
from test_api import wait


@pytest.mark.parametrize("style", ["waveform", "spectrum"])
def test_real_ffmpeg_preview_and_export(client, audio, style, tmp_path):
    assert client.get("/api/capabilities").json()["render_ready"]
    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    design = data["config"]
    design.update(visualizer=style, preset="ultrafast")
    assert client.patch(url + "/config", headers=headers, json=design).status_code == 200
    assert client.post(url + "/preview", headers=headers, json={"start": 0}).status_code == 409
    client.post(url + "/background/approve", headers=headers)
    assert client.post(url + "/preview", headers=headers, json={"start": 0.75}).status_code == 200
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    path = store.jobs[data["id"]].path / "preview.mp4"
    assert abs(float(probe(path)["format"]["duration"]) - 4.25) < 0.25
    script = (path.parent / "subtitles.ass").read_text(encoding="utf-8")
    assert "0:00:00.00,0:00:01.25" in script
    client.post(url + "/preview/approve", headers=headers)
    assert client.post(url + "/render", headers=headers).status_code == 200
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    video = path.parent / "video.mp4"
    assert abs(float(probe(video)["format"]["duration"]) - 5) < 0.25
    frames = []
    for i, t in enumerate([0.3, 1.3, 2.3, 4.8]):
        out = tmp_path / f"{i}.png"
        subprocess.run(
            [settings.ffmpeg, "-v", "error", "-ss", str(t), "-i", str(video), "-frames:v", "1", str(out)],
            check=True,
        )
        with Image.open(out) as im:
            frames.append(im.convert("RGB"))
    silence, tone, silence2, after = frames
    region = (170, 565, 1750, 720)
    difference = ImageStat.Stat(ImageChops.difference(silence.crop(region), tone.crop(region))).mean
    assert sum(difference) > 0.5
    quiet_difference = ImageStat.Stat(ImageChops.difference(silence.crop(region), silence2.crop(region))).mean
    assert sum(quiet_difference) < sum(difference) * 0.5
    assert sum(silence.getpixel((500, 600))) > 30
    caption_region = (200, 850, 1720, 1030)
    assert (
        sum(
            ImageStat.Stat(
                ImageChops.difference(silence.crop(caption_region), tone.crop(caption_region))
            ).mean
        )
        > 0.5
    )
    assert (
        sum(
            ImageStat.Stat(
                ImageChops.difference(silence.crop(caption_region), after.crop(caption_region))
            ).mean
        )
        < 1
    )
    rms = []
    for timestamp in (0.2, 1.2):
        decoded = subprocess.check_output(
            [
                settings.ffmpeg,
                "-v",
                "error",
                "-ss",
                str(timestamp),
                "-i",
                str(video),
                "-t",
                "0.1",
                "-vn",
                "-ac",
                "1",
                "-ar",
                "44100",
                "-f",
                "s16le",
                "pipe:1",
            ]
        )
        samples = array("h", decoded)
        rms.append((sum(v * v for v in samples) / len(samples)) ** 0.5)
    assert rms[0] < 100 and rms[1] > 1000
    response = client.get(url + "/artifacts/video?download=true", headers=headers)
    assert response.status_code == 200 and response.headers["content-type"] == "video/mp4"
    assert "attachment" in response.headers["content-disposition"]


def test_cancel_then_retry(client, audio):
    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    client.post(url + "/background/approve", headers=headers)
    client.post(url + "/preview", headers=headers, json={"start": 0})
    client.post(url + "/cancel", headers=headers)
    assert wait(client, url, headers)["state"] == "cancelled"
    assert "preview" not in store.jobs[data["id"]].artifacts
    client.post(url + "/preview", headers=headers, json={"start": 4.7})
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
