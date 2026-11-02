"""Small local pipeline for debugging; outputs are explicitly retained by the user."""

import argparse
import shutil
import sys
import tempfile
import threading
import time
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.media import validate_audio, local_background, normalize_image, render
from app.models import Design
from app.subtitles import parse_srt
from app.config import settings

parser = argparse.ArgumentParser()
parser.add_argument("--audio", type=Path, required=True)
parser.add_argument("--srt", type=Path, required=True)
parser.add_argument("--image", type=Path)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--start", type=float, default=0)
parser.add_argument("--seconds", type=float, default=20)
parser.add_argument("--style", choices=["waveform", "spectrum"], default="waveform")
args = parser.parse_args()
if args.output.exists():
    parser.error("La salida ya existe; elige otro nombre.")
meta = validate_audio(args.audio)
if not 0 <= args.start < meta["duration"] or args.seconds <= 0:
    parser.error("Inicio/duración inválidos.")
cues, _ = parse_srt(args.srt.read_bytes())
args.output.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="easypodcast-cli-") as folder:
    path = Path(folder)
    shutil.copyfile(args.audio, path / "audio.bin")
    if args.image:
        normalize_image(args.image, path / "background.png")
    else:
        local_background(path / "background.png")
    job = SimpleNamespace(
        path=path,
        meta=meta,
        cues=cues,
        cancel=threading.Event(),
        process=None,
        active_deadline=time.time() + settings.active_ttl_seconds,
    )
    render(
        job,
        Design(visualizer=args.style),
        args.start,
        min(args.seconds, meta["duration"] - args.start),
        path / "result.mp4",
        lambda p: None,
    )
    shutil.copyfile(path / "result.mp4", args.output)
print("MP4 validado:", args.output)
