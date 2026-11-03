import subprocess
from io import BytesIO

import pytest
from app.config import settings
from app.fonts import FONTS, font_path, logo_position
from app.jobs import store
from app.models import Design
from app.subtitles import Cue, make_ass
from PIL import Image
from pydantic import ValidationError
from test_api import wait


@pytest.mark.parametrize("font", ["sans", "serif", "mono"])
def test_styles_use_selected_fonts_and_sizes(font):
    design = Design(
        title="Clear English", title_font=font, subtitle_font=font, title_font_size=82, font_size=36
    )
    script = make_ass([Cue(0, 1, "¿Cómo estás?")], design, 1)
    assert f"Style: Title,{FONTS[font][0]},82," in script
    assert f"Style: Default,{FONTS[font][0]},36," in script
    assert font_path(font).is_file()


@pytest.mark.parametrize(
    "values",
    [
        {"title_font": "evil,Arial"},
        {"subtitle_font": "../../font"},
        {"title_font_size": 500},
        {"logo_position": "movie=evil"},
        {"logo_margin": -3},
    ],
)
def test_style_validation(values):
    with pytest.raises(ValidationError):
        Design(**values)


def test_logo_positions_and_defaults():
    assert logo_position(Design()) == ("W-w-40", "40")
    assert logo_position(Design(logo_position="bottom-left", logo_margin=70)) == ("70", "H-h-70")
    assert logo_position(Design(logo_position="middle-right")) == ("W-w-40", "(H-h)/2")


def test_public_fonts_are_allowlisted(client):
    for key in FONTS:
        response = client.get("/api/fonts/" + key)
        assert response.status_code == 200 and response.headers["content-type"] == "font/ttf"
    assert client.get("/api/fonts/unknown").status_code == 404


@pytest.mark.parametrize("position", ["top-left", "bottom-right"])
def test_logo_and_fonts_in_real_render(client, audio, position, tmp_path):
    logo = BytesIO()
    Image.new("RGBA", (100, 100), (255, 0, 255, 255)).save(logo, format="PNG")
    response = client.post(
        "/api/jobs",
        files={
            "audio": ("demo.wav", audio),
            "srt": ("demo.srt", b"1\n00:00:00,000 --> 00:00:02,000\nClear English"),
            "logo": ("logo.png", logo.getvalue(), "image/png"),
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    headers = {"X-Job-Token": data["token"]}
    url = "/api/jobs/" + data["id"]
    assert "logo" in data["artifacts"]
    assert client.get(url + "/artifacts/logo", headers=headers).status_code == 200
    design = Design(
        title="Clear English",
        title_font="serif",
        subtitle_font="mono",
        title_font_size=82,
        font_size=36,
        title_offset_x=-200 if position == "top-left" else 200,
        title_offset_y=80,
        logo_position=position,
        logo_margin=70,
        preset="ultrafast",
    )
    assert client.patch(url + "/config", headers=headers, json=design.model_dump()).status_code == 200
    client.post(url + "/background/approve", headers=headers)
    client.post(url + "/preview", headers=headers, json={"start": 4})
    result = wait(client, url, headers)
    assert result["state"] == "completed", result
    image = tmp_path / "logo.png"
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
        pixel = frame.convert("RGB").getpixel((120, 120) if position == "top-left" else (1800, 960))
        assert pixel[0] > 180 and pixel[1] < 70 and pixel[2] > 180


@pytest.mark.parametrize("x,y", [(-600, -80), (0, 0), (600, 150)])
def test_title_position_is_rendered_and_roundtrips(x, y):
    design = Design(title="Hello", title_offset_x=x, title_offset_y=y)
    script = make_ass([], design, 1)
    assert rf"{chr(92)}pos({960 + x},{100 + y})" in script
    assert Design.model_validate(design.model_dump()).title_offset_x == x


@pytest.mark.parametrize(
    "values", [{"title_offset_x": 601}, {"title_offset_y": -81}, {"title_offset_y": 401}]
)
def test_title_position_bounds(values):
    with pytest.raises(ValidationError):
        Design(**values)


def test_title_position_respects_visualizer_space():
    with pytest.raises(ValueError, match="posición"):
        make_ass([], Design(title_offset_y=400, title_font_size=110), 1)
    assert Design.model_validate({"title": "Old JSON"}).title_offset_y == 0
