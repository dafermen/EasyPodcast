from pathlib import Path

FONT_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"
FONTS = {
    "sans": ("DejaVu Sans", "DejaVuSans.ttf"),
    "serif": ("DejaVu Serif", "DejaVuSerif.ttf"),
    "mono": ("DejaVu Sans Mono", "DejaVuSansMono.ttf"),
    "nunito": ("Nunito", "Nunito-Regular.ttf"),
    "fredoka": ("Fredoka", "Fredoka-Regular.ttf"),
    "quicksand": ("EasyPodcast Rounded", "EasyPodcastRounded-Regular.ttf"),
    "poppins": ("Poppins", "Poppins-Regular.ttf"),
    "baloo2": ("Baloo 2", "Baloo2-Regular.ttf"),
    "outfit": ("Outfit", "Outfit-Regular.ttf"),
    "balsamiqsans": ("Balsamiq Sans", "BalsamiqSans-Regular.ttf"),
    "lexend": ("Lexend", "Lexend-Regular.ttf"),
    "atkinsonhyperlegible": ("Atkinson Hyperlegible", "AtkinsonHyperlegible-Regular.ttf"),
    "comicneue": ("Comic Neue", "ComicNeue-Regular.ttf"),

}
BOLD_FILES = {
    "sans": "DejaVuSans-Bold.ttf",
    "serif": "DejaVuSerif-Bold.ttf",
    "mono": "DejaVuSansMono-Bold.ttf",
    **{
        key: filename.replace("-Regular.ttf", "-Bold.ttf")
        for key, (_, filename) in FONTS.items()
        if key not in {"sans", "serif", "mono"}
    },
}


def font_path(key, bold=False):
    return FONT_DIR / (BOLD_FILES[key] if bold else FONTS[key][1])


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
