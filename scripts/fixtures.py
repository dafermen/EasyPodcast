"""Synthetic local silence/tone and SRT; no personal recordings."""

import argparse
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.config import settings

parser = argparse.ArgumentParser()
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--seconds", type=int, default=26)
args = parser.parse_args()
if not 2 <= args.seconds <= 7200:
    parser.error("--seconds debe estar entre 2 y 7200")
args.output.mkdir(parents=True, exist_ok=True)
subprocess.run(
    [
        settings.ffmpeg,
        "-v",
        "error",
        "-y",
        "-f",
        "lavfi",
        "-i",
        rf"aevalsrc=if(lt(mod(t\,2)\,1)\,0\,0.35*sin(2*PI*440*t)):s=44100:d={args.seconds}",
        str(args.output / "demo.wav"),
    ],
    check=True,
)


def stamp(t):
    return f"{t // 3600:02}:{t // 60 % 60:02}:{t % 60:02},000"


blocks = []
for i, t in enumerate(range(0, args.seconds, 4), 1):
    blocks.append(
        f"{i}\n{stamp(t)} --> {stamp(min(t + 3, args.seconds))}\n¿Listos? Canción, acentos y {{llaves}}. Barra \\N literal."
    )
(args.output / "demo.srt").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
print("Archivos sintéticos creados en", args.output)
