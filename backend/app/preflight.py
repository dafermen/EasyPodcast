"""Pre-render layout review using the actual font measurement and ASS generation rules."""

from PIL import Image, ImageFont

from .fonts import font_path
from .subtitles import clip_cues, make_ass, wrap_text


def overlaps(a, b):
    """Return whether two pixel rectangles have a positive-area intersection."""
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def inspect(job):
    """Report blockers and warnings; never charge providers or start an encoder."""
    design = job.design
    width, height = design.frame_size
    blockers, warnings = [], list(job.warnings)
    try:
        make_ass(clip_cues(job.cues, 0, job.meta["duration"]), design, job.meta["duration"])
    except ValueError as exc:
        blockers.append(str(exc))
    if not job.cues or not job.subtitles_approved:
        blockers.append("Review and approve subtitles before rendering.")
    if job.cues and max(c.end for c in job.cues) > job.meta["duration"] and not design.trim_subtitles:
        blockers.append("Allow trimming subtitles that extend beyond the audio.")
    x, y = width / 2 + design.title_offset_x, 100 + design.title_offset_y
    title_width = max(80, min(1600, 2 * (min(x, width - x) - 120)))
    title_lines = wrap_text(
        design.title, design.title_font, design.title_font_size, title_width, design.title_bold
    )
    font = ImageFont.truetype(str(font_path(design.title_font, design.title_bold)), design.title_font_size)
    title_width = max((font.getlength(line) for line in title_lines), default=0)
    title = (x - title_width / 2, y, x + title_width / 2, y + len(title_lines) * design.title_font_size * 1.3)
    subtitle_top = height - design.subtitle_margin - design.font_size * design.max_lines * 1.25 - 20
    if (job.path / "logo.png").exists():
        with Image.open(job.path / "logo.png") as image:
            lw, lh = (v * design.logo_scale for v in image.size)
        lx = width - lw - design.logo_margin if design.logo_position.endswith("right") else design.logo_margin
        ly = (
            (height - lh) / 2
            if design.logo_position.startswith("middle")
            else height - lh - design.logo_margin
            if design.logo_position.startswith("bottom")
            else design.logo_margin
        )
        if design.logo_x is not None:
            lx = min(width - lw, max(0, width * design.logo_x))
        if design.logo_y is not None:
            ly = min(height - lh, max(0, height * design.logo_y))
        logo = (lx, ly, lx + lw, ly + lh)
        if min(lx, ly) < 0 or lw > width or lh > height:
            blockers.append("Logo is outside the frame. Reduce its size or margin.")
        if design.title and overlaps(title, logo):
            warnings.append("Logo may overlap the title. Review the preview.")
        if overlaps(logo, (0, subtitle_top, width, height)):
            warnings.append("Logo may overlap subtitles. Review the preview.")
        if overlaps(
            logo,
            (
                width / 12,
                height * design.wave_y,
                width * 11 / 12,
                height * (design.wave_y + design.wave_height),
            ),
        ):
            warnings.append("Logo may overlap the visualizer. Review the preview.")
    if design.output_format != "landscape":
        warnings.append(
            "Background is fitted with padding to preserve faces. Review this format before export."
        )
    return {
        "ready": not blockers,
        "blockers": blockers,
        "warnings": list(dict.fromkeys(warnings)),
        "width": width,
        "height": height,
    }
