import json
import math
import os
import shutil
import signal
import subprocess
import time
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .config import settings
from .subtitles import clip_cues, make_ass

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets" / "fonts"


def run(args, timeout=30):
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        check=True,
        shell=False,
    )


def capabilities():
    result = {
        "ffmpeg": bool(shutil.which(settings.ffmpeg)),
        "ffprobe": bool(shutil.which(settings.ffprobe)),
        "filters": {},
        "h264": False,
        "aac": False,
        "font": (FONTS / "DejaVuSans.ttf").is_file(),
        "image_provider": bool(settings.openai_api_key and settings.image_model),
        "limits": {
            "audio_bytes": settings.max_audio_bytes,
            "srt_bytes": settings.max_srt_bytes,
            "image_bytes": settings.max_image_bytes,
            "pixels": settings.max_pixels,
            "duration_seconds": settings.max_duration,
            "queue": settings.queue_size,
            "concurrent_renders": 1,
            "jobs": settings.max_jobs,
        },
    }
    if result["ffmpeg"]:
        try:
            filters = run([settings.ffmpeg, "-hide_banner", "-filters"]).stdout
            encoders = run([settings.ffmpeg, "-hide_banner", "-encoders"]).stdout
            result["filters"] = {
                f: f" {f} " in filters for f in ("ass", "showwaves", "showfreqs", "colorkey", "overlay")
            }
            result["h264"] = "libx264" in encoders
            result["aac"] = " aac " in encoders
        except (OSError, subprocess.SubprocessError):
            pass
    result["render_ready"] = (
        result["ffmpeg"]
        and result["ffprobe"]
        and result["h264"]
        and result["aac"]
        and result["font"]
        and all(result["filters"].values())
    )
    return result


def probe(path: Path):
    return json.loads(
        run(
            [
                settings.ffprobe,
                "-v",
                "error",
                "-protocol_whitelist",
                "file,pipe",
                "-format_whitelist",
                "mp3,wav,mov",
                "-show_format",
                "-show_streams",
                "-of",
                "json",
                str(path),
            ]
        ).stdout
    )


def validate_audio(path: Path):
    try:
        meta = probe(path)
        streams = [s for s in meta["streams"] if s["codec_type"] == "audio"]
        duration = float(meta["format"]["duration"])
        formats = set(meta["format"]["format_name"].split(","))
        if not streams or not math.isfinite(duration) or not 0 < duration <= settings.max_duration:
            raise ValueError("Duración inválida o superior al límite; se necesita una pista de audio.")
        if not formats.intersection({"mp3", "wav", "mov", "mp4", "m4a"}):
            raise ValueError("Se admiten contenidos MP3, WAV y M4A.")
        return {
            "duration": duration,
            "audio_stream": streams[0]["index"],
            "audio_tracks": len(streams),
            "codec": streams[0]["codec_name"],
        }
    except (KeyError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        raise ValueError("No se pudo verificar el audio con FFprobe.") from exc


def normalize_image(source: Path, target: Path, logo=False):
    try:
        with Image.open(source) as im:
            if im.format not in ({"PNG"} if logo else {"PNG", "JPEG"}):
                raise ValueError("Usa PNG para el logo, o PNG/JPEG para el fondo.")
            if im.width * im.height > settings.max_pixels or min(im.size) < 16:
                raise ValueError("Dimensiones de imagen fuera de los límites.")
            im.load()
            image = ImageOps.exif_transpose(im).convert("RGBA" if logo else "RGB")
            if logo:
                image.thumbnail((300, 160))
            else:
                # Contain with margins avoids cropping faces or stretching the source.
                image = ImageOps.pad(image, (1920, 1080), color="#101522")
            image.save(target, "PNG")
    except (OSError, Image.DecompressionBombError) as exc:
        raise ValueError("Imagen ilegible o demasiado grande.") from exc


def local_background(target: Path):
    image = Image.new("RGB", (1920, 1080), "#101522")
    draw = ImageDraw.Draw(image)
    for y in range(1080):
        draw.line((0, y, 1920, y), fill=(16 + int(y / 100), 21 + int(y / 80), 34 + int(y / 55)))
    draw.ellipse((-240, 260, 480, 980), outline="#234752", width=3)
    draw.ellipse((1440, -300, 2240, 500), outline="#755353", width=3)
    draw.line((160, 350, 1760, 350), fill="#334155", width=2)
    image.save(target)


def terminate(process):
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=15)
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    process.wait(timeout=15)


def render(job, design, start, duration, output, update):
    import threading

    cues = clip_cues(job.cues, start, duration)
    (job.path / "subtitles.ass").write_text(make_ass(cues, design, duration), encoding="utf-8")
    # All paths in filters are controlled relative filenames: Windows drive syntax never enters the graph.
    fonts = job.path / "fonts"
    fonts.mkdir(exist_ok=True)
    shutil.copyfile(FONTS / "DejaVuSans.ttf", fonts / "DejaVuSans.ttf")
    size = f"1600x{round(1080 * design.wave_height) // 2 * 2}"
    color = "0x" + design.color[1:]
    visual = (
        f"showwaves=s={size}:mode=line:rate=30:colors={color}"
        if design.visualizer == "waveform"
        else f"showfreqs=s={size}:mode=bar:ascale=sqrt:fscale=log:colors={color}:rate=30"
    )
    graph = (
        f"[1:{job.meta['audio_stream']}]asplit=2[aout][viz];"
        f"[viz]volume={design.sensitivity},{visual},format=rgba,colorkey=0x000000:0.03:0.0[wave];"
        f"[0:v][wave]overlay=160:{round(1080 * design.wave_y)}:shortest=1[base];"
    )
    inputs = [
        settings.ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y",
        "-loop",
        "1",
        "-framerate",
        "30",
        "-i",
        "background.png",
        "-ss",
        str(start),
        "-i",
        "audio.bin",
    ]
    if (job.path / "logo.png").exists():
        inputs += ["-i", "logo.png"]
        graph += "[base][2:v]overlay=W-w-60:40[branded];[branded]"
    else:
        graph += "[base]"
    graph += "ass=subtitles.ass:fontsdir=fonts,format=yuv420p[v]"
    args = inputs + [
        "-filter_complex",
        graph,
        "-map",
        "[v]",
        "-map",
        "[aout]",
        "-t",
        str(duration),
        "-r",
        "30",
        "-c:v",
        "libx264",
        "-preset",
        design.preset,
        "-crf",
        str(design.crf),
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        "-threads",
        "2",
        "-filter_complex_threads",
        "2",
        "-progress",
        "pipe:1",
        "-nostats",
        output.name,
    ]
    logs = deque(maxlen=40)
    process = subprocess.Popen(
        args,
        cwd=job.path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
        start_new_session=os.name != "nt",
    )
    job.process = process

    def read_progress():
        for line in process.stdout:
            if line.startswith("out_time_us="):
                try:
                    update(min(0.99, int(line.split("=")[1]) / 1_000_000 / duration))
                except ValueError:
                    pass

    def read_errors():
        for line in process.stderr:
            logs.append(line[-1000:])

    readers = [
        threading.Thread(target=read_progress, daemon=True),
        threading.Thread(target=read_errors, daemon=True),
    ]
    for reader in readers:
        reader.start()
    try:
        while process.poll() is None:
            if job.cancel.is_set():
                terminate(process)
                raise InterruptedError("Operación cancelada.")
            if time.time() > job.active_deadline:
                terminate(process)
                raise ValueError("El trabajo superó el límite de tiempo activo.")
            if shutil.disk_usage(job.path).free < settings.min_free_bytes:
                terminate(process)
                raise ValueError("Espacio libre insuficiente durante el render.")
            time.sleep(0.15)
        for reader in readers:
            reader.join(timeout=5)
        if process.returncode:
            # No user input or internal filesystem paths exposed in API errors.
            raise ValueError("FFmpeg no pudo completar el video. Comprueba dependencias y formatos.")
        result = probe(output)
        videos = [s for s in result["streams"] if s["codec_type"] == "video"]
        audios = [s for s in result["streams"] if s["codec_type"] == "audio"]
        v = videos[0]
        if (
            v["codec_name"] != "h264"
            or v["width"] != 1920
            or v["height"] != 1080
            or v["pix_fmt"] != "yuv420p"
            or v["avg_frame_rate"] != "30/1"
            or not audios
            or audios[0]["codec_name"] != "aac"
            or abs(float(result["format"]["duration"]) - duration) > 0.25
        ):
            raise ValueError("El archivo exportado no superó la validación multimedia.")
    finally:
        if process.poll() is None:
            terminate(process)
        job.process = None
        for reader in readers:
            reader.join(timeout=5)
        process.stdout.close()
        process.stderr.close()
