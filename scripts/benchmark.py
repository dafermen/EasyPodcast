"""Manual reproducible long synthetic render; requires optional psutil in the venv."""

import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import threading
import time
from types import SimpleNamespace

import psutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.media import render, validate_audio, local_background, probe
from app.models import Design
from app.subtitles import parse_srt
from app.config import settings

parser = argparse.ArgumentParser()
parser.add_argument("--minutes", type=int, default=30)
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--preset", choices=["veryfast", "ultrafast", "fast", "medium"], default="veryfast")
args = parser.parse_args()
if not 30 <= args.minutes <= 60:
    parser.error("The benchmark must last between 30 and 60 minutes.")
args.output.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[1]
subprocess.run(
    [
        sys.executable,
        str(root / "scripts" / "fixtures.py"),
        "--output",
        str(args.output),
        "--seconds",
        str(args.minutes * 60),
    ],
    check=True,
)
audio = args.output / "demo.wav"
audio.rename(args.output / "audio.bin")
meta = validate_audio(args.output / "audio.bin")
cues, _ = parse_srt((args.output / "demo.srt").read_bytes())
local_background(args.output / "background.png")
job = SimpleNamespace(
    path=args.output.resolve(),
    meta=meta,
    cues=cues,
    cancel=threading.Event(),
    process=None,
    active_deadline=time.time() + settings.active_ttl_seconds,
)
design = Design(title="EasyPodcast synthetic benchmark", preset=args.preset)
started = time.monotonic()
samples = []
done = threading.Event()
parent = psutil.Process(os.getpid())


def monitor():
    """Sample process-tree RSS/CPU and managed disk until the benchmark finishes."""
    last_print = 0
    while not done.wait(0.5):
        processes = [parent] + parent.children(recursive=True)
        rss = cpu = 0
        for process in processes:
            try:
                rss += process.memory_info().rss
                times = process.cpu_times()
                cpu += times.user + times.system
            except psutil.Error:
                pass
        disk = sum(p.stat().st_size for p in args.output.rglob("*") if p.is_file())
        samples.append({"elapsed": time.monotonic() - started, "rss": rss, "cpu_seconds": cpu, "disk": disk})
        if time.monotonic() - last_print > 20:
            print(f"Benchmark: {samples[-1]['elapsed']:.0f} s, RAM {rss / 1024**2:.0f} MiB", flush=True)
            last_print = time.monotonic()


thread = threading.Thread(target=monitor, daemon=True)
thread.start()
try:
    render(job, design, 0, meta["duration"], args.output.resolve() / "benchmark.mp4", lambda p: None)
finally:
    done.set()
    thread.join()
elapsed = time.monotonic() - started
result = {
    "system": platform.platform(),
    "python": platform.python_version(),
    "logical_cpus": psutil.cpu_count(),
    "preset": args.preset,
    "crf": design.crf,
    "audio_seconds": meta["duration"],
    "wall_seconds": elapsed,
    "peak_rss_mib": max(s["rss"] for s in samples) / 1024**2,
    "peak_managed_disk_mib": max(s["disk"] for s in samples) / 1024**2,
    "peak_observed_cpu_seconds": max(s["cpu_seconds"] for s in samples),
    "cpu_measurement": "Cumulative process CPU sampled; child exit can lower last sample. Not whole-system CPU.",
    "ffmpeg": subprocess.check_output([settings.ffmpeg, "-version"], text=True).splitlines()[0],
    "output": probe(args.output.resolve() / "benchmark.mp4"),
}
(args.output / "benchmark.json").write_text(
    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(json.dumps({k: v for k, v in result.items() if k != "output"}, ensure_ascii=False, indent=2))
