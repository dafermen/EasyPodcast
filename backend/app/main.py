"""FastAPI endpoints, local request guards and authenticated artifact responses."""

import asyncio
import hmac
import shutil
import time
from contextlib import asynccontextmanager
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware

from .config import settings
from .jobs import ACTIVE, make_job, store
from .media import ROOT, capabilities, local_background, normalize_image, validate_audio
from .models import Design, PreviewRequest, SubtitleEdit, TranscriptionOptions
from .subtitles import parse_srt
from .uploads import receive_files


@asynccontextmanager
async def lifespan(app):
    """Start the store and compute capabilities at startup; close resources during shutdown."""
    store.start()
    app.state.upload_slot = asyncio.Semaphore(1)
    app.state.capabilities = await asyncio.to_thread(capabilities)
    yield
    await asyncio.to_thread(store.close)


app = FastAPI(title="EasyPodcast", version="0.4.1", lifespan=lifespan)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])


class RequestGuard:
    """Enforce allowed browser origins and a total request-body byte budget."""

    def __init__(self, app):
        """Initialize the instance resources; background threads are started separately."""
        self.app = app

    async def __call__(self, scope, receive, send):
        """Handle an ASGI request while preserving middleware or response cleanup guarantees."""
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        origin = headers.get(b"origin", b"").decode()
        method = scope["method"]
        if (origin and origin not in settings.allowed_origins) or (
            method not in {"GET", "HEAD", "OPTIONS"} and origin not in settings.allowed_origins
        ):
            return await JSONResponse({"detail": "Origen no permitido."}, 403)(scope, receive, send)
        total = 0
        limit = settings.max_audio_bytes + settings.max_srt_bytes + settings.max_image_bytes * 2 + 1024**2

        async def bounded_receive():
            """Count streamed ASGI body bytes and enforce the total upload budget."""
            nonlocal total
            message = await receive()
            total += len(message.get("body", b""))
            if total > limit:
                raise HTTPException(413, "La carga supera el límite total.")
            return message

        await self.app(scope, bounded_receive, send)


app.add_middleware(RequestGuard)


@app.exception_handler(ValueError)
async def invalid(request, exc):
    """Convert a validation ValueError into a safe HTTP 422 response."""
    return JSONResponse({"detail": str(exc)}, status_code=422)


@app.get("/api/health")
def health():
    """Expose service liveness and version without secrets."""
    return {"status": "ok", "version": "0.4.1"}


@app.get("/api/capabilities")
def get_capabilities(request: Request):
    """Return dependency and limit checks computed at application startup."""
    return request.app.state.capabilities


def get_job(jid: str, request: Request):
    """Authenticate the job token and reject absent, expired or invalid sessions."""
    with store.lock:
        job = store.jobs.get(jid)
        token = request.headers.get("X-Job-Token", "")
        # Cookies authenticate media navigation only; API requests always require an explicit header.
        if "/artifacts/" in request.url.path:
            token = token or request.cookies.get(f"ep_{jid}", "")
        if not job or not token or not hmac.compare_digest(token, job.token):
            raise HTTPException(
                404,
                "El episodio ya no está disponible o la sesión no es válida. Puede haber vencido o perdido sus archivos al reiniciar el servidor. Vuelve a cargar los archivos.",
            )
        if job.deleting or (job.state not in ACTIVE and time.time() > job.expires):
            raise HTTPException(
                410, "El episodio venció o fue eliminado. Vuelve a cargar los archivos para continuar."
            )
        return job


def editable(job):
    """Reject edits while an operation or artifact download holds the job."""
    if job.state in ACTIVE or job.readers:
        raise HTTPException(409, "Espera a que termine la operación o descarga activa.")


@app.post(
    "/api/jobs",
    status_code=201,
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "type": "object",
                        "required": ["audio"],
                        "properties": {
                            name: {"type": "string", "format": "binary"}
                            for name in ["audio", "srt", "image", "logo"]
                        },
                    }
                }
            },
        }
    },
)
async def create_job(
    request: Request,
    subtitle_mode: Literal["upload", "generate"] = "upload",
    language: Literal["auto", "en", "es", "pt", "fr", "de", "it"] = "en",
    model: Literal["tiny", "base"] = "tiny",
):
    """Serialize uploads and dispatch creation for the selected subtitle source."""
    if request.app.state.upload_slot.locked():
        raise HTTPException(429, "Ya hay una carga en curso.")
    async with request.app.state.upload_slot:
        return await create_uploaded_job(
            request, subtitle_mode, TranscriptionOptions(language=language, model=model)
        )


async def create_uploaded_job(request, subtitle_mode, options):
    """Receive and validate uploads, create an episode and optionally queue local transcription."""
    from .transcription import available

    if subtitle_mode == "generate" and not available():
        raise HTTPException(
            409, "El motor de transcripción local no está instalado. Ejecuta npm ci en transcription."
        )
    with store.lock:
        if len(store.jobs) >= settings.max_jobs:
            raise HTTPException(429, "Elimina un trabajo anterior o espera a que venza.")
    jid, path = store.new_path()
    try:
        try:
            async with asyncio.timeout(settings.failure_ttl_seconds):
                files = await receive_files(request, path, require_srt=subtitle_mode == "upload")
        except TimeoutError as exc:
            raise HTTPException(408, "La carga incompleta superó el plazo permitido.") from exc
        meta = await asyncio.to_thread(validate_audio, path / "audio.bin")
        if subtitle_mode == "generate" and "srt" in files:
            raise ValueError("Elige generar subtítulos o cargar SRT, no ambas opciones.")
        cues, warnings = (
            parse_srt((path / "original.srt").read_bytes()) if subtitle_mode == "upload" else ([], [])
        )
        if meta["audio_tracks"] > 1:
            warnings.append("Hay varias pistas; se usará la primera pista de audio.")
        if cues and max(c.end for c in cues) > meta["duration"]:
            warnings.append(
                "Hay subtítulos posteriores al audio. Activa el recorte explícito para renderizar."
            )
        if "image" in files:
            await asyncio.to_thread(normalize_image, path / "image.bin", path / "background.png")
            (path / "image.bin").unlink()
        else:
            await asyncio.to_thread(local_background, path / "background.png")
        if "logo" in files:
            await asyncio.to_thread(normalize_image, path / "logo.bin", path / "logo.png", True)
            (path / "logo.bin").unlink()
        job = make_job(jid, path, meta, cues, warnings)
        if "logo" in files:
            job.artifacts.add("logo")
        job.subtitle_source = subtitle_mode
        job.subtitles_approved = subtitle_mode == "upload"
        job.transcription_options = options
        if subtitle_mode == "upload":
            job.artifacts.add("subtitles")
        job.background_mode = "upload" if "image" in files else "local"
        with store.lock:
            if len(store.jobs) >= settings.max_jobs:
                raise HTTPException(429, "Límite de trabajos alcanzado.")
            store.jobs[jid] = job
            if subtitle_mode == "generate":
                try:
                    store.enqueue(job, "transcript")
                except BaseException:
                    del store.jobs[jid]
                    raise
        response = JSONResponse({**job.public(), "token": job.token}, status_code=201)
        response.set_cookie(
            f"ep_{jid}",
            job.token,
            httponly=True,
            samesite="strict",
            path=f"/api/jobs/{jid}/artifacts",
            max_age=settings.active_ttl_seconds + settings.ttl_seconds,
        )
        return response
    except BaseException:
        store.remove_path(path)
        raise


@app.get("/api/jobs/{jid}")
def status(response: Response, job=Depends(get_job)):
    """Return a job snapshot and refresh the media cookie only to its existing expiry."""
    with store.lock:
        # Keep media authentication aligned with the real deadline. Polling never extends job TTL.
        deadline = job.active_deadline + settings.ttl_seconds if job.state in ACTIVE else job.expires
        response.set_cookie(
            f"ep_{job.id}",
            job.token,
            httponly=True,
            samesite="strict",
            path=f"/api/jobs/{job.id}/artifacts",
            max_age=max(1, int(deadline - time.time())),
        )
        return job.public()


@app.patch("/api/jobs/{jid}/config")
def configure(design: Design, job=Depends(get_job)):
    """Replace validated Design settings and invalidate previous approvals/artifacts."""
    with store.lock:
        editable(job)
        store.invalidate(job)
        job.design = design
        return job.public()


@app.post("/api/jobs/{jid}/background")
def generate(job=Depends(get_job)):
    """Queue explicit optional provider generation for the current job."""
    if not settings.openai_api_key or not settings.image_model:
        raise HTTPException(409, "Proveedor sin configurar; usa fondo local o propio.")
    store.enqueue(job, "background")
    return job.public()


@app.post("/api/jobs/{jid}/background/approve")
def approve_background(job=Depends(get_job)):
    """Mark the current background reviewed without generating or rendering anything."""
    with store.lock:
        editable(job)
        job.approved = True
        return job.public()


@app.post("/api/jobs/{jid}/preview/approve")
def approve_preview(job=Depends(get_job)):
    """Mark the current preview reviewed after checking that it exists."""
    with store.lock:
        editable(job)
        if "preview" not in job.artifacts:
            raise HTTPException(409, "Primero genera y revisa una prueba.")
        job.preview_approved = True
        return job.public()


def check_render(job):
    """Enforce dependencies, subtitle/background approval, trim permission and disk budget."""
    if not job.cues or not job.subtitles_approved:
        raise HTTPException(409, "Genera y revisa los subtítulos antes de renderizar.")
    if not capabilities()["render_ready"]:
        raise HTTPException(409, "Faltan dependencias multimedia; consulta el diagnóstico.")
    if not job.approved:
        raise HTTPException(409, "Revisa y aprueba el fondo actual.")
    if max(c.end for c in job.cues) > job.meta["duration"] and not job.design.trim_subtitles:
        raise HTTPException(409, "Autoriza el recorte de subtítulos que exceden el audio.")
    # Conservative product budget, not a measured size estimate.
    required = settings.min_free_bytes + int(job.meta["duration"] * 1_000_000)
    if shutil.disk_usage(job.path).free < required:
        raise HTTPException(507, "Espacio libre insuficiente según el presupuesto preventivo de exportación.")


@app.post("/api/jobs/{jid}/preview")
def preview(body: PreviewRequest, job=Depends(get_job)):
    """Queue up to 20 seconds from the validated starting offset."""
    with store.lock:
        editable(job)
        check_render(job)
        if body.start >= job.meta["duration"]:
            raise ValueError("El inicio debe ser anterior al final del audio.")
        store.enqueue(job, "preview", body.start)
        return job.public()


@app.post("/api/jobs/{jid}/render")
def export(job=Depends(get_job)):
    """Queue full-episode export only after the current preview has been approved."""
    with store.lock:
        editable(job)
        check_render(job)
        if not job.preview_approved:
            raise HTTPException(409, "Revisa y aprueba una prueba con la configuración actual.")
        store.enqueue(job, "video")
        return job.public()


@app.post("/api/jobs/{jid}/cancel")
def cancel(job=Depends(get_job)):
    """Signal cancellation and expose a cancelling phase without blocking the API."""
    with store.lock:
        if job.state in ACTIVE:
            job.cancel.set()
            job.state, job.phase = "cancelling", "Cancelando operación"
        return job.public()


@app.delete("/api/jobs/{jid}")
def delete(job=Depends(get_job)):
    """Request cancellation and deferred deletion of this managed episode."""
    with store.lock:
        job.deleting = True
        job.cancel.set()
        store.cleanup()
    return {"deleted": True}


@app.get("/api/jobs/{jid}/artifacts/{kind}")
def artifact(kind: str, download: bool = False, job=Depends(get_job)):
    """Serve an allowlisted artifact, holding a reader lease for media streaming."""
    with store.lock:
        if kind == "config":
            return JSONResponse(
                job.design.model_dump(),
                headers={
                    "Content-Disposition": 'attachment; filename="easypodcast-design.json"',
                    "Cache-Control": "no-store",
                },
            )
        mapping = {
            "logo": ("logo.png", "image/png"),
            "subtitles": (
                "generated.srt" if job.subtitle_source == "generate" else "original.srt",
                "application/x-subrip",
            ),
            "background": ("background.png", "image/png"),
            "preview": ("preview.mp4", "video/mp4"),
            "video": ("video.mp4", "video/mp4"),
        }
        if kind not in mapping or kind not in job.artifacts:
            raise HTTPException(404, "Artefacto no disponible.")
        if job.state in ACTIVE:
            raise HTTPException(409, "Espera a que termine la operación activa.")
        name, mime = mapping[kind]
        job.readers += 1

    def release():
        """Release one download reader and retry deferred cleanup."""
        with store.lock:
            job.readers -= 1
        store.cleanup()

    class LeasedFileResponse(FileResponse):
        """Release a download reader lease even when response streaming fails or disconnects."""

        async def __call__(self, scope, receive, send):
            """Handle an ASGI request while preserving middleware or response cleanup guarantees."""
            try:
                await super().__call__(scope, receive, send)
            finally:
                release()

    return LeasedFileResponse(
        job.path / name,
        media_type=mime,
        filename=name if download else None,
        headers={"Cache-Control": "no-store"},
    )


@app.post("/api/jobs/{jid}/transcribe")
def retry_transcription(job=Depends(get_job)):
    """Queue transcription again only for episodes created in generate mode."""
    if job.subtitle_source != "generate":
        raise HTTPException(409, "Este trabajo usa un SRT propio; crea otro con generación automática.")
    store.enqueue(job, "transcript")
    return job.public()


@app.get("/api/jobs/{jid}/subtitles")
def subtitles(job=Depends(get_job)):
    """Read the reviewable SRT and expose whether word timestamps exist."""
    with store.lock:
        if job.state in ACTIVE:
            raise HTTPException(409, "Espera a que termine la operación activa.")
        if not job.cues:
            raise HTTPException(409, "Aún no hay subtítulos disponibles.")
        path = job.path / ("generated.srt" if job.subtitle_source == "generate" else "original.srt")
        return {
            "srt": path.read_text(encoding="utf-8-sig"),
            "word_timestamps": any(c.words for c in job.cues),
        }


@app.put("/api/jobs/{jid}/subtitles")
def edit_subtitles(body: SubtitleEdit, job=Depends(get_job)):
    """Validate edited SRT, drop stale word timing and invalidate previous renders."""
    if len(body.srt.encode("utf-8")) > settings.max_srt_bytes:
        raise HTTPException(413, "El SRT supera el límite permitido.")
    cues, warnings = parse_srt(body.srt.encode())
    with store.lock:
        editable(job)
        path = job.path / ("generated.srt" if job.subtitle_source == "generate" else "original.srt")
        if path.exists() and path.read_text(encoding="utf-8-sig") == body.srt:
            return job.public()
        path.write_text(body.srt, encoding="utf-8")
        job.cues = cues
        job.warnings = warnings + [
            "SRT editado: se desactiva resaltado por palabra para no usar tiempos desactualizados."
        ]
        job.subtitles_approved = False
        job.artifacts.add("subtitles")
        store.invalidate(job)
        return job.public()


@app.post("/api/jobs/{jid}/subtitles/approve")
def approve_subtitles(job=Depends(get_job)):
    """Approve generated or edited cues so the user can proceed to design."""
    with store.lock:
        editable(job)
        if not job.cues:
            raise HTTPException(409, "Aún no hay subtítulos para revisar.")
        job.subtitles_approved = True
        return job.public()


@app.get("/api/fonts/{key}")
def font_file(key: str, bold: bool = False):
    """Serve an allowlisted bundled font and reject arbitrary path requests."""
    from .fonts import FONTS, font_path

    if key not in FONTS:
        raise HTTPException(404, "Fuente no disponible.")
    return FileResponse(
        font_path(key, bold), media_type="font/ttf", headers={"Cache-Control": "public, max-age=86400"}
    )


frontend = ROOT / "frontend" / "dist"
if frontend.is_dir():
    app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
