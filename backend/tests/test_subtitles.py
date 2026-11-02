import pytest
from app.models import Design, PreviewRequest
from app.subtitles import Cue, clip_cues, escape_ass, make_ass, parse_srt
from pydantic import ValidationError


def test_unicode_bom_overlap_and_html():
    cues, warnings = parse_srt(
        "\ufeff1\n00:00:00,000 --> 00:00:02,000\n<b>¿Cómo estás?</b>\n\n2\n00:00:01,500 --> 00:00:03,000\n¡Bien!".encode()
    )
    assert cues[0].text == "¿Cómo estás?"
    assert len(warnings) == 1


@pytest.mark.parametrize(
    "data",
    [
        b"",
        b"\xff",
        b"1\n00:00:02,000 --> 00:00:01,000\nx",
        b"1\n-00:00:00,000 --> 00:00:01,000\nx",
        b"1\n00:60:00,000 --> 01:00:00,000\nx",
        b"1\n00:00:00,000 --> 00:00:01,000\n<b></b>",
    ],
)
def test_invalid_srt(data):
    with pytest.raises(ValueError):
        parse_srt(data)


def test_fragment_clips_both_boundaries():
    clipped = clip_cues([Cue(0, 6, "inicio"), Cue(20, 30, "final"), Cue(40, 50, "fuera")], 5, 20)
    assert clipped == [Cue(0, 1, "inicio"), Cue(15, 20, "final")]


def test_ass_does_not_allow_overrides_or_control_sequences():
    escaped = escape_ass(r"{\pos(0,0)} C:\New\notes")
    assert r"\{" in escaped and "\\N" not in escaped and "\u2060" in escaped
    script = make_ass([Cue(0, 1, "á\n¿sí?")], Design(title=""), 1)
    assert r"á\N¿sí?" in script


@pytest.mark.parametrize(
    "config",
    [
        {"color": "red;movie=evil"},
        {"sensitivity": float("nan")},
        {"font_size": 1000},
        {"wave_y": -1},
        {"unknown": 1},
    ],
)
def test_design_limits(config):
    with pytest.raises(ValidationError):
        Design(**config)


def test_preview_finite():
    with pytest.raises(ValidationError):
        PreviewRequest(start=float("inf"))


def test_layout_reserves_space_for_subtitles():
    with pytest.raises(ValidationError, match="superponen"):
        Design(wave_y=0.65, wave_height=0.22, font_size=72, max_lines=3)
