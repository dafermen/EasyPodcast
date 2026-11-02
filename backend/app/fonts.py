from pathlib import Path

FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
FONTS = {
    "sans": ("DejaVu Sans", "DejaVuSans.ttf"),
    "serif": ("DejaVu Serif", "DejaVuSerif.ttf"),
    "mono": ("DejaVu Sans Mono", "DejaVuSansMono.ttf"),
}


def font_path(key):
    return FONT_DIR / FONTS[key][1]


def logo_position(design):
    margin = design.logo_margin
    x = "W-w-" + str(margin) if design.logo_position.endswith("right") else str(margin)
    if design.logo_position.startswith("top"):
        y = str(margin)
    elif design.logo_position.startswith("bottom"):
        y = "H-h-" + str(margin)
    else:
        y = "(H-h)/2"
    return x, y
