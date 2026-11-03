"""Pydantic request contracts; UI types alone are not server validation."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FontKey = Literal[
    "sans",
    "serif",
    "mono",
    "nunito",
    "fredoka",
    "quicksand",
    "poppins",
    "baloo2",
    "outfit",
    "balsamiqsans",
    "lexend",
    "atkinsonhyperlegible",
    "comicneue",
]


class Design(BaseModel):
    """Validate the complete episode appearance and encoding settings at the API boundary."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    # Episode title drawn in the video; never translated by the interface locale.
    output_format: Literal["landscape", "portrait", "square"] = "landscape"
    logo_x: float | None = Field(None, ge=0, le=1)
    logo_y: float | None = Field(None, ge=0, le=1)
    logo_scale: float = Field(1, ge=0.25, le=2.5)
    title: str = Field("My episode", max_length=120)
    # Optional visual context sent only to an explicitly selected image provider.
    description: str = Field("", max_length=1200)
    # Allowlisted image-generation style, not an arbitrary instruction.
    image_style: Literal["illustration", "realistic"] = "illustration"
    # User-authored visual palette/context; independent of interface language.
    atmosphere: str = Field("Cozy studio, blue and coral", max_length=300)
    # Choose waveform or frequency spectrum for the audio-reactive layer.
    visualizer: Literal["waveform", "spectrum"] = "waveform"
    # Visualizer color as a strict RGB hex value.
    color: str = Field("#5EEAD4", pattern=r"^#[0-9a-fA-F]{6}$")
    # Gain on the visual analysis branch, not the exported sound volume.
    sensitivity: float = Field(1, ge=0.2, le=4)
    # Visualizer top position as a fraction of the 1080-pixel canvas height.
    wave_y: float = Field(0.52, ge=0.3, le=0.65)
    # Visualizer height as a fraction of the canvas height.
    wave_height: float = Field(0.16, ge=0.06, le=0.22)
    # Subtitle font size in 1080p video pixels.
    font_size: int = Field(48, ge=28, le=72)
    # Allowlisted bundled subtitle font family ID.
    subtitle_font: FontKey = "sans"
    # Allowlisted bundled title font family ID.
    title_font: FontKey = "sans"
    # Select the real Bold title weight when enabled.
    title_bold: bool = True
    # Title font size in 1080p video pixels.
    title_font_size: int = Field(64, ge=28, le=110)
    # Horizontal offset from the centered title anchor, in pixels; negative moves left.
    title_offset_x: int = Field(0, ge=-600, le=600)
    # Vertical offset from the original 100-pixel title top, in pixels; negative moves up.
    title_offset_y: int = Field(0, ge=-80, le=400)
    # One of six allowlisted edge/vertical logo placements.
    logo_position: Literal[
        "top-left", "top-right", "middle-left", "middle-right", "bottom-left", "bottom-right"
    ] = "top-right"
    # Logo inset from the selected canvas edge, in video pixels.
    logo_margin: int = Field(40, ge=20, le=160)
    # Subtitle RGB hex color; text is still escaped separately for ASS.
    subtitle_color: str = Field("#FFFFFF", pattern=r"^#[0-9a-fA-F]{6}$")
    # Subtitle outline thickness in video pixels.
    outline: int = Field(3, ge=1, le=6)
    # Subtitle bottom inset in video pixels.
    subtitle_margin: int = Field(80, ge=40, le=180)
    # Fraction of canvas width allowed for subtitle wrapping.
    subtitle_width: float = Field(0.85, ge=0.5, le=0.9)
    # Maximum wrapped subtitle lines; excessive text raises an error rather than truncating.
    max_lines: int = Field(2, ge=2, le=3)
    # H.264 constant-rate-factor quality; lower values increase quality/file size.
    crf: int = Field(21, ge=18, le=28)
    # Allowlisted encoder speed/compression tradeoff.
    preset: Literal["ultrafast", "veryfast", "fast", "medium"] = "veryfast"
    # Explicit permission to clip cues extending beyond the audio.
    trim_subtitles: bool = False
    # Highlight estimated active words only when trustworthy timing exists.
    highlight_words: bool = True
    # RGB hex color for the currently active recognized word.
    highlight_color: str = Field("#FFD54A", pattern=r"^#[0-9a-fA-F]{6}$")

    @property
    def frame_size(self):
        """Return output dimensions; all layout units are pixels in this frame."""
        return {"landscape": (1920, 1080), "portrait": (1080, 1920), "square": (1080, 1080)}[
            self.output_format
        ]

    @model_validator(mode="after")
    def safe_layout(self):
        """Reject subtitle and visualizer overlap using canvas-coordinate layout estimates."""
        height = self.frame_size[1]
        subtitle_top = height - self.subtitle_margin - self.font_size * self.max_lines * 1.25 - 20
        if height * (self.wave_y + self.wave_height) > subtitle_top:
            raise ValueError("Onda y subtítulos se superponen: reduce altura/posición, letra o líneas.")
        return self


class PreviewRequest(BaseModel):
    """Validate the nonnegative preview start time in seconds."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    # Preview start offset in seconds, not a duration.
    start: float = Field(0, ge=0)


class TranscriptionOptions(BaseModel):
    """Allowlist the local Whisper model and spoken audio language."""

    model_config = ConfigDict(extra="forbid")
    # Spoken language for local Whisper; independent of the interface locale.
    language: Literal["auto", "en", "es", "pt", "fr", "de", "it"] = "en"
    # Local Whisper size profile: Tiny is faster, Base is generally more demanding.
    model: Literal["tiny", "base"] = "tiny"


class SubtitleEdit(BaseModel):
    """Bound the size of an edited SRT payload."""

    model_config = ConfigDict(extra="forbid")
    # Edited UTF-8 SRT payload; saving edits drops estimated word alignment.
    srt: str = Field(min_length=1, max_length=5 * 1024**2)


class DraftRequest(BaseModel):
    """Version a recovery draft against the last saved design to reject stale in-flight autosaves."""

    model_config = ConfigDict(extra="forbid")
    design: Design
    base: Design


class TemplateRequest(BaseModel):
    """Optional human-readable brand name; never used as a directory or filename."""

    model_config = ConfigDict(extra="forbid")
    title: str = Field(min_length=1, max_length=120)
