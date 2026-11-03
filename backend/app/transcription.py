"""Isolated local Whisper inference. Never sends source audio to a service."""

import json
import os
import shutil
import subprocess
import threading
import time

from .config import settings
from .media import ROOT, terminate
from .subtitles import Cue, Word, render_srt


def available():
    """Check the Node executable and installed local inference package without downloading models."""
    return bool(
        shutil.which(settings.node)
        and (ROOT / "transcription/node_modules/@huggingface/transformers/package.json").is_file()
    )


def supervise(job, args, on_event=None):
    """Run FFmpeg or Node while monitoring cancellation, timeout, disk space and JSON progress."""
    process = subprocess.Popen(
        args,
        cwd=job.path,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
        start_new_session=os.name != "nt",
    )
    job.process = process

    def read():
        """Drain child-process JSON events and ignore malformed or oversized event lines."""
        for line in process.stdout:
            if on_event and len(line) < 8192:
                try:
                    on_event(json.loads(line))
                except (ValueError, KeyError, TypeError):
                    pass

    reader = threading.Thread(target=read, daemon=True)
    reader.start()
    try:
        while process.poll() is None:
            if job.cancel.is_set():
                raise InterruptedError()
            if time.time() > job.active_deadline:
                raise ValueError("La transcripción superó el tiempo activo permitido.")
            if shutil.disk_usage(job.path).free < settings.min_free_bytes:
                raise ValueError("No hay espacio libre suficiente para transcribir.")
            time.sleep(0.15)
        if job.cancel.is_set():
            raise InterruptedError()
        if process.returncode:
            raise ValueError(
                "La transcripción local falló. Revisa instalación, conexión para descargar el modelo e idioma; puedes reintentar o usar SRT propio."
            )
    finally:
        if process.poll() is None:
            terminate(process)
        reader.join(timeout=5)
        process.stdout.close()
        job.process = None


def transcript_cues(data, duration):
    """Validate recognized words and group them into readable subtitle cues."""
    raw = data.get("words", [])
    if not raw or len(raw) > 150_000:
        raise ValueError("No se detectaron palabras con tiempos válidos.")
    words = []
    for item in raw:
        word = Word.model_validate(item)
        if word.end > duration + 0.05 or (words and word.start < words[-1].end):
            raise ValueError("El motor devolvió tiempos de palabra inválidos.")
        words.append(word)
    cues = []
    group = []
    for word in words:
        if group and (
            len(group) >= 8
            or len(" ".join(w.text for w in group)) + len(word.text) > 64
            or word.end - group[0].start > 6
            or word.start - group[-1].end > 1
        ):
            cues.append(Cue(group[0].start, group[-1].end, " ".join(w.text for w in group), tuple(group)))
            group = []
        group.append(word)
    if group:
        cues.append(Cue(group[0].start, group[-1].end, " ".join(w.text for w in group), tuple(group)))
    return cues


def transcribe(job):
    """Convert audio, run local inference, validate results and remove PCM/JSON intermediates."""
    if not available():
        raise ValueError(
            "Instala el motor local con npm ci en la carpeta transcription y reinicia EasyPodcast."
        )
    pcm = job.path / "speech.f32"
    result = job.path / "transcript.partial.json"
    try:
        job.phase = "Preparando audio para transcripción"
        job.progress = None
        supervise(
            job,
            [
                settings.ffmpeg,
                "-v",
                "error",
                "-nostdin",
                "-y",
                "-protocol_whitelist",
                "file,pipe",
                "-format_whitelist",
                "mp3,wav,mov",
                "-i",
                "audio.bin",
                "-map",
                f"0:{job.meta['audio_stream']}",
                "-vn",
                "-ac",
                "1",
                "-ar",
                "16000",
                "-f",
                "f32le",
                str(pcm),
            ],
        )

        def event(data):
            """Convert worker phase/progress events into safe job status updates."""
            if data.get("phase") == "loading_model":
                job.phase = "Cargando modelo local (primera vez: descarga de Hugging Face)"
                job.progress = None
            elif data.get("phase") == "transcribing":
                processed = float(data["processed_seconds"])
                job.phase = "Transcribiendo audio localmente"
                job.progress = max(0, min(0.99, processed / job.meta["duration"]))

        supervise(
            job,
            [
                settings.node,
                str(ROOT / "transcription/worker.mjs"),
                str(pcm),
                str(result),
                job.transcription_options.model,
                job.transcription_options.language,
                str(settings.transcription_cache),
                str(settings.transcription_allow_download).lower(),
            ],
            event,
        )
        if result.stat().st_size > settings.max_srt_bytes * 8:
            raise ValueError("La transcripción supera el límite permitido.")
        cues = transcript_cues(json.loads(result.read_text(encoding="utf-8")), job.meta["duration"])
        srt = render_srt(cues)
        if len(srt.encode()) > settings.max_srt_bytes:
            raise ValueError("El SRT generado supera el límite.")
        return cues, srt
    finally:
        pcm.unlink(missing_ok=True)
        result.unlink(missing_ok=True)
