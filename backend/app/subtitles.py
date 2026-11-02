import html
import re
import textwrap
from dataclasses import dataclass


@dataclass(frozen=True)
class Cue:
    start: float
    end: float
    text: str


TIME = r"(\d{2,}):([0-5]\d):([0-5]\d)[,.](\d{3})"
TIMING = re.compile(rf"^{TIME}\s+-->\s+{TIME}\s*$")


def parse_srt(data: bytes) -> tuple[list[Cue], list[str]]:
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
    return [
        Cue(max(c.start, start) - start, min(c.end, start + duration) - start, c.text)
        for c in cues
        if c.end > start and c.start < start + duration
    ]


def escape_ass(text: str) -> str:
    # libass supports \{ and \}. A zero-width word joiner after original backslashes
    # prevents \N/\n/\h interpretation while preserving the visible literal glyph.
    text = "".join(c for c in text if c == "\n" or ord(c) >= 32)
    return text.replace("\\", "\\\u2060").replace("{", r"\{").replace("}", r"\}").replace("\n", r"\N")


def wrap_caption(text, design):
    from pathlib import Path

    from PIL import ImageFont

    font_path = Path(__file__).resolve().parents[2] / "assets" / "fonts" / "DejaVuSans.ttf"
    font = ImageFont.truetype(str(font_path), design.font_size)
    width = 1920 * design.subtitle_width - 40
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
    if len(output) > design.max_lines:
        raise ValueError(
            f"Un subtítulo requiere {len(output)} líneas. Acorta el SRT, reduce la letra o permite tres líneas."
        )
    return "\n".join(output)


def ass_time(seconds: float) -> str:
    cs = max(0, round(seconds * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02}:{cs // 100 % 60:02}.{cs % 100:02}"


def make_ass(cues, design, duration: float) -> str:
    color = design.subtitle_color.lstrip("#")
    color = "&H00" + color[4:6] + color[2:4] + color[0:2]
    margin = round(1920 * (1 - design.subtitle_width) / 2)
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,{design.font_size},{color},&H000000FF,&H00101522,&H80000000,0,0,0,0,100,100,0,0,1,{design.outline},1,2,{margin},{margin},{design.subtitle_margin},1
Style: Title,DejaVu Sans,64,&H00FFFFFF,&H000000FF,&H00101522,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,120,120,100,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    if design.title:
        title = "\n".join(textwrap.wrap(design.title, width=44))
        events.append(f"Dialogue: 1,0:00:00.00,{ass_time(duration)},Title,,0,0,0,,{escape_ass(title)}")
    for cue in cues:
        caption = wrap_caption(cue.text, design)
        events.append(
            f"Dialogue: 0,{ass_time(cue.start)},{ass_time(cue.end)},Default,,0,0,0,,{escape_ass(caption)}"
        )
    return header + "\n".join(events) + "\n"
