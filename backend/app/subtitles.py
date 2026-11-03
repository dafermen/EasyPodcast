"""SRT/ASS timing, wrapping, escaping and estimated current-word highlighting."""

import html
import re
from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .fonts import FONTS, font_path


class Word(BaseModel):
    """Validate one recognized word with start/end times in seconds."""

    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    start: float = Field(ge=0)
    end: float = Field(gt=0)
    text: str = Field(min_length=1, max_length=200)

    @model_validator(mode="after")
    def valid_interval(self):
        """Require visible word text and an end time strictly after the start."""
        if self.end <= self.start or not self.text.strip():
            raise ValueError("Intervalo de palabra inválido.")
        return self


@dataclass(frozen=True)
class Cue:
    """Represent one subtitle interval and optional word timing needed for highlighting."""

    start: float
    end: float
    text: str
    words: tuple[Word, ...] = ()
    word_offset: int = 0


TIME = r"(\d{2,}):([0-5]\d):([0-5]\d)[,.](\d{3})"
TIMING = re.compile(rf"^{TIME}\s+-->\s+{TIME}\s*$")


def parse_srt(data: bytes) -> tuple[list[Cue], list[str]]:
    """Decode UTF-8 SRT, validate ordered intervals and return cues plus review warnings."""
    try:
        content = data.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n").strip()
    except UnicodeDecodeError as exc:
        raise ValueError(
            "El SRT debe estar codificado en UTF-8. Convierte el archivo e inténtalo otra vez."
        ) from exc
    if not content:
        raise ValueError("El SRT está vacío.")
    cues, warnings = [], []
    for block in re.split(r"\n\s*\n", content):
        lines = block.splitlines()
        if lines and lines[0].strip().isdigit():
            lines.pop(0)
        match = TIMING.fullmatch(lines[0].strip()) if lines else None
        if not match or len(lines) < 2:
            raise ValueError(f"Formato SRT inválido en el bloque {len(cues) + 1}.")
        n = list(map(int, match.groups()))
        start = n[0] * 3600 + n[1] * 60 + n[2] + n[3] / 1000
        end = n[4] * 3600 + n[5] * 60 + n[6] + n[7] / 1000
        if end <= start or (cues and start < cues[-1].start):
            raise ValueError("Los tiempos deben estar ordenados y el final debe superar el inicio.")
        text = html.unescape(re.sub(r"<[^>]*>", "", "\n".join(lines[1:])))
        text = "".join(c for c in text if c in "\n\t" or ord(c) >= 32).replace("\t", " ")
        if not text.strip():
            raise ValueError("Hay un subtítulo sin texto visible.")
        if cues and start < cues[-1].end:
            warnings.append(f"Solapamiento en el subtítulo {len(cues) + 1}.")
        if len(text) > 100 or len(text.splitlines()) > 2:
            warnings.append(f"Texto denso en el subtítulo {len(cues) + 1}; revisa la prueba.")
        cues.append(Cue(start, end, text))
    return cues, warnings


def clip_cues(cues: list[Cue], start: float, duration: float) -> list[Cue]:
    """Intersect cues/words with the preview interval and shift timing to the new zero point."""
    return [
        Cue(
            max(c.start, start) - start,
            min(c.end, start + duration) - start,
            c.text,
            tuple(
                Word(start=max(w.start, start) - start, end=min(w.end, start + duration) - start, text=w.text)
                for w in c.words
                if w.end > start and w.start < start + duration
            ),
            c.word_offset + sum(len("".join(w.text.split())) for w in c.words if w.end <= start),
        )
        for c in cues
        if c.end > start and c.start < start + duration
    ]


def escape_ass(text: str) -> str:
    # libass supports \{ and \}. A zero-width word joiner after original backslashes
    # prevents \N/\n/\h interpretation while preserving the visible literal glyph.
    """Escape literal user text so ASS override syntax cannot be injected."""
    text = "".join(c for c in text if c == "\n" or ord(c) >= 32)
    return text.replace("\\", "\\\u2060").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def wrap_text(text, font_key, size, width, bold=False):
    """Measure the selected real font and split text into lines within the pixel width."""
    from PIL import ImageFont

    font = ImageFont.truetype(str(font_path(font_key, bold)), size)
    output = []
    for paragraph in text.splitlines():
        remaining = paragraph
        while font.getlength(remaining) > width:
            count = 1
            while count < len(remaining) and font.getlength(remaining[: count + 1]) <= width:
                count += 1
            split = remaining.rfind(" ", 0, count + 1)
            if split <= 0:
                split = count
            output.append(remaining[:split])
            remaining = remaining[split:].lstrip(" ")
        output.append(remaining)
    return output


def wrap_caption(text, design):
    """Wrap subtitle text and reject layouts exceeding the selected line limit."""
    output = wrap_text(
        text, design.subtitle_font, design.font_size, design.frame_size[0] * design.subtitle_width - 40
    )
    if len(output) > design.max_lines:
        raise ValueError(
            f"Un subtítulo requiere {len(output)} líneas. Acorta el SRT, reduce la letra o permite tres líneas."
        )
    return "\n".join(output)


def ass_time(seconds: float) -> str:
    """Format seconds as nonnegative ASS centisecond timestamps."""
    cs = max(0, round(seconds * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def render_srt(cues):
    """Serialize cues using numbered UTF-8 SRT blocks and millisecond timestamps."""

    def stamp(seconds):
        """Format seconds as a subtitle timestamp for a generated fixture or SRT."""
        ms = round(seconds * 1000)
        return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"

    return (
        "\n\n".join(f"{i}\n{stamp(c.start)} --> {stamp(c.end)}\n{c.text}" for i, c in enumerate(cues, 1))
        + "\n"
    )


def ass_color(value):
    """Convert a validated RGB hex color into ASS BGR notation."""
    value = value.lstrip("#")
    return "&H" + value[4:6] + value[2:4] + value[0:2] + "&"


def highlighted_caption(caption, words, active, design, offset=0):
    # Map by visible characters so line breaks do not shift the active word.
    """Color only the active word while preserving escaped text and clipped offsets."""
    low = offset + sum(len("".join(w.text.split())) for w in words[:active])
    high = low + len("".join(words[active].text.split()))
    result = []
    position = 0
    colored = False
    for char in caption:
        want = low <= position < high
        if not char.isspace() and want != colored:
            result.append(r"{\c" + ass_color(design.highlight_color if want else design.subtitle_color) + "}")
            colored = want
        result.append(escape_ass(char))
        if not char.isspace():
            position += 1
    return "".join(result)


def make_ass(cues, design, duration: float) -> str:
    """Build the complete subtitle/title ASS document at 1920 by 1080 resolution."""
    color = design.subtitle_color.lstrip("#")
    color = "&H00" + color[4:6] + color[2:4] + color[0:2]
    frame_width, frame_height = design.frame_size
    margin = round(frame_width * (1 - design.subtitle_width) / 2)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {frame_width}
PlayResY: {frame_height}
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONTS[design.subtitle_font][0]},{design.font_size},{color},&H000000FF,&H00101522,&H80000000,0,0,0,0,100,100,0,0,1,{design.outline},1,2,{margin},{margin},{design.subtitle_margin},1
Style: Title,{FONTS[design.title_font][0]},{design.title_font_size},&H00FFFFFF,&H000000FF,&H00101522,&H80000000,{-1 if design.title_bold else 0},0,0,0,100,100,0,0,1,3,0,8,120,120,100,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    if design.title:
        x, y = frame_width // 2 + design.title_offset_x, 100 + design.title_offset_y
        width = min(1600, 2 * (min(x, frame_width - x) - 120))
        if width < 80 or y < 0:
            raise ValueError("Title is outside the frame. Reduce its offset.")
        lines = wrap_text(design.title, design.title_font, design.title_font_size, width, design.title_bold)
        if (
            len(lines) > 3
            or y + len(lines) * design.title_font_size * 1.3 > frame_height * design.wave_y - 20
        ):
            raise ValueError(
                "El título no cabe sobre el visualizador: reduce su tamaño, acorta el texto o ajusta su posición."
            )
        title = "\n".join(lines)
        position = rf"{{\an8\pos({x},{y})}}"
        events.append(
            f"Dialogue: 1,0:00:00.00,{ass_time(duration)},Title,,0,0,0,,{position}{escape_ass(title)}"
        )
    for cue in cues:
        caption = wrap_caption(cue.text, design)
        boundaries = sorted(
            {
                cue.start,
                cue.end,
                *[max(cue.start, min(cue.end, t)) for w in cue.words for t in (w.start, w.end)],
            }
        )
        if not design.highlight_words or not cue.words:
            boundaries = [cue.start, cue.end]
        for begin, end in zip(boundaries, boundaries[1:]):
            if ass_time(begin) == ass_time(end):
                continue
            middle = (begin + end) / 2
            active = next((i for i, w in enumerate(cue.words) if w.start <= middle < w.end), None)
            line = (
                highlighted_caption(caption, cue.words, active, design, cue.word_offset)
                if design.highlight_words and active is not None
                else escape_ass(caption)
            )
            events.append(f"Dialogue: 0,{ass_time(begin)},{ass_time(end)},Default,,0,0,0,,{line}")
    return header + "\n".join(events) + "\n"
