from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Design(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    title: str = Field("Mi episodio", max_length=120)
    description: str = Field("", max_length=1200)
    image_style: Literal["illustration", "realistic"] = "illustration"
    atmosphere: str = Field("Estudio acogedor, azul y coral", max_length=300)
    visualizer: Literal["waveform", "spectrum"] = "waveform"
    color: str = Field("#5EEAD4", pattern=r"^#[0-9a-fA-F]{6}$")
    sensitivity: float = Field(1, ge=0.2, le=4)
    wave_y: float = Field(0.52, ge=0.3, le=0.65)
    wave_height: float = Field(0.16, ge=0.06, le=0.22)
    font_size: int = Field(48, ge=28, le=72)
    subtitle_font: Literal["sans", "serif", "mono"] = "sans"
    title_font: Literal["sans", "serif", "mono"] = "sans"
    title_font_size: int = Field(64, ge=28, le=110)
    logo_position: Literal[
        "top-left", "top-right", "middle-left", "middle-right", "bottom-left", "bottom-right"
    ] = "top-right"
    logo_margin: int = Field(40, ge=20, le=160)
    subtitle_color: str = Field("#FFFFFF", pattern=r"^#[0-9a-fA-F]{6}$")
    outline: int = Field(3, ge=1, le=6)
    subtitle_margin: int = Field(80, ge=40, le=180)
    subtitle_width: float = Field(0.85, ge=0.5, le=0.9)
    max_lines: int = Field(2, ge=2, le=3)
    crf: int = Field(21, ge=18, le=28)
    preset: Literal["ultrafast", "veryfast", "fast", "medium"] = "veryfast"
    trim_subtitles: bool = False
    highlight_words: bool = True
    highlight_color: str = Field("#FFD54A", pattern=r"^#[0-9a-fA-F]{6}$")

    @model_validator(mode="after")
    def safe_layout(self):
        subtitle_top = 1080 - self.subtitle_margin - self.font_size * self.max_lines * 1.25 - 20
        if 1080 * (self.wave_y + self.wave_height) > subtitle_top:
            raise ValueError("Onda y subtítulos se superponen: reduce altura/posición, letra o líneas.")
        return self


class PreviewRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    start: float = Field(0, ge=0)


class TranscriptionOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")
    language: Literal["auto", "en", "es", "pt", "fr", "de", "it"] = "en"
    model: Literal["tiny", "base"] = "tiny"


class SubtitleEdit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    srt: str = Field(min_length=1, max_length=5 * 1024**2)
