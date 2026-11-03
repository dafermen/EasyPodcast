import subprocess

import pytest
from app.fonts import FONTS, font_path
from app.jobs import store
from app.models import Design
from app.subtitles import make_ass
from conftest import create
from PIL import Image, ImageChops, ImageStat
from test_api import wait


@pytest.mark.parametrize("family", ["nunito", "fredoka", "quicksand", "poppins"])
@pytest.mark.parametrize("bold", [False, True])
def test_fonts_and_bold_styles(family, bold, client):
    design = Design(title_font=family, subtitle_font=family, title_bold=bold)
    script = make_ass([], design, 1)
    title = next(line for line in script.splitlines() if line.startswith("Style: Title,"))
    assert title.split(",")[7] == ("-1" if bold else "0")
    assert FONTS[family][0] in title
    assert font_path(family, bold).is_file()
    assert client.get(f"/api/fonts/{family}?bold={str(bold).lower()}").status_code == 200


def test_old_design_keeps_bold_title():
    assert Design.model_validate({"title": "Old design"}).title_bold is True


@pytest.mark.parametrize("family", ["nunito", "fredoka", "quicksand", "poppins"])
def test_real_fonts_render_both_weights(client, audio, family, tmp_path):
    from app.config import settings

    data, headers = create(client, audio)
    url = "/api/jobs/" + data["id"]
    pictures = []
    for bold in (False, True):
        design = Design(
            title="Clear English",
            title_font=family,
            subtitle_font=family,
            title_font_size=82,
            title_bold=bold,
            preset="ultrafast",
        )
        client.patch(url + "/config", headers=headers, json=design.model_dump()).raise_for_status()
        client.post(url + "/background/approve", headers=headers).raise_for_status()
        client.post(url + "/preview", headers=headers, json={"start": 4}).raise_for_status()
        result = wait(client, url, headers)
        assert result["state"] == "completed", result
        image = tmp_path / f"{bold}.png"
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
            pictures.append(frame.convert("RGB").crop((200, 90, 1720, 260)))
    assert sum(ImageStat.Stat(ImageChops.difference(*pictures)).mean) > 0.3

