# Local HTTP API

Base URL: http://127.0.0.1:8000/api. Interactive schema: /docs; JSON schema: /openapi.json. These generated schemas are authoritative for field types and bounds.

Mutations require an allowed Origin, for example http://127.0.0.1:8000. Job API calls require X-Job-Token. Artifact navigation may also use a job-specific HttpOnly cookie. Do not put tokens in URLs. There is no public job-list endpoint.

| Method and path | Behavior |
| --- | --- |
| GET /health | Status and version, without secrets |
| GET /capabilities | Dependencies, encoders, filters, fonts, provider availability, transcription and retention limits |
| POST /jobs | Multipart audio; SRT required in upload mode; image/logo optional. Query subtitle_mode=upload/generate, language=en/auto/es/pt/fr/de/it, model=tiny/base. Returns 201, job and token |
| GET /jobs/{id} | Snapshot: state, phase, progress, errors, warnings, metadata, config, approvals, artifacts, expires_at |
| PATCH /jobs/{id}/config | Complete Design document; omitted fields take defaults, not a partial merge |
| POST /jobs/{id}/background | Explicitly queue provider generation; preserve earlier background if it fails |
| POST /jobs/{id}/background/approve | Approve current background |
| POST /jobs/{id}/preview | Body {"start":0}; queue at most 20 seconds |
| POST /jobs/{id}/preview/approve | Approve current rendered preview |
| POST /jobs/{id}/render | Queue full export; requires approved background and preview |
| POST /jobs/{id}/cancel | Request idempotent cancellation |
| DELETE /jobs/{id} | Request cancellation and deferred managed deletion |
| GET /jobs/{id}/artifacts/{kind} | background, logo, subtitles, preview, video or config. download=true requests download; media supports Range |
| POST /jobs/{id}/transcribe | Retry a generate-mode transcription |
| GET /jobs/{id}/subtitles | Read SRT and timing availability |
| PUT /jobs/{id}/subtitles | Body {"srt":"..."}; validate and invalidate previous renders; changed text loses word timing |
| POST /jobs/{id}/subtitles/approve | Enable design after review |
| GET /fonts/{key}?bold=false | Public allowlisted local TTF; no arbitrary filesystem access |

State enums remain English in both UI languages. The UI translates legacy backend phase/error messages for display; raw API consumers should treat messages as explanatory text, not stable machine codes. Interface locale and theme are not part of Design and are not sent as audio-language settings.

Retention metadata: completed_seconds=86400, failed_seconds=900, active_seconds=14400 and survives_restart=false by default. GET status refreshes the media cookie only to the job's existing expiry, without extending the job TTL.

Errors include 400 invalid Host, 403 Origin, 404 missing job/token/artifact, 408 incomplete-upload deadline, 409 busy/dependencies/approvals, 410 expired job before cleanup, 413 size, 422 validation/queue explanation, 429 upload/job capacity and 507 disk space. Unknown or invalid fields, non-finite numbers, unsupported enums and unsafe colors are rejected.

```python
import httpx
with httpx.Client(base_url="http://127.0.0.1:8000", headers={"Origin": "http://127.0.0.1:8000"}) as client:
    with open("episode.wav", "rb") as audio, open("episode.srt", "rb") as srt:
        response = client.post("/api/jobs", files={"audio": audio, "srt": srt})
        response.raise_for_status()
        job = response.json()
    headers = {"X-Job-Token": job["token"]}
    snapshot = client.get(f'/api/jobs/{job["id"]}', headers=headers).json()
```

Store the token only as long as needed. JSON export contains no secret key, media file, token or resumable session.

## Durable studio endpoints

POST /library/session requires an allowed Origin and sets the HttpOnly `ep_library` cookie scoped to /api. The following library endpoints require it; job-specific routes additionally require X-Job-Token. A cookie-only artifact request can access original audio for the cue editor, using the same lease/Range behavior as other media.

| Method and path | Behavior |
| --- | --- |
| GET /projects | Cover IDs, title, created/updated Unix timestamps, checkpoint/live state and recovery-draft indicator; no tokens/paths |
| GET /projects/{id}/thumbnail | Small normalized cover image |
| POST /projects/{id}/open | Reuse an idle session or rebuild from durable data; return Job plus in-memory token and media cookie |
| POST /projects/{id}/duplicate | Create an independent saved project and workspace |
| PUT /projects/{id}/draft | Body {design: Design, base: Design}; save only if base matches the last saved config; saved=false indicates a stale request |
| GET /templates | Local brand template summaries |
| POST /jobs/{id}/templates | Optional JSON {"title":"Brand name"}; save clean visual settings and background/logo, without audio/SRT |
| POST /jobs/{id}/templates/{templateId} | Apply brand media/settings while retaining episode title/description/subtitles; clear approvals |
| GET /jobs/{id}/preflight | {ready, blockers, warnings, width, height}; real font/ASS checks, no encoder/provider call |
| GET /jobs/{id}/artifacts/audio | Original selected audio input for subtitle playback; token or media cookie required |

Job snapshots add project_id and archive_error. Design adds output_format (landscape/portrait/square), logo_x/logo_y normalized free top-left coordinates (null restores presets), and logo_scale 0.25–2.5. Older design files default to landscape, preset logo placement and scale 1. Subtitle GET also returns structured cues. DELETE job closes only its temporary workspace; the durable project remains. A failed archival checkpoint can block a destructive close with 507 so the only working copy is not discarded.
