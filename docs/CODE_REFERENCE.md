# Source code reference

Generated inventory of application/utility classes, named functions, parameters and assigned variables by lexical scope. Read JUNIOR_GUIDE.md first for a guided walkthrough. Test fixture internals, imported dependencies and third-party code are outside this inventory. Tiny loop locals are described by their source assignment rather than fictional domain meanings. Source excerpts remain exact code, so legacy Spanish message keys are code, not English documentation prose.

Regenerate with `python scripts/build_code_reference.py` after installing frontend dependencies. Source line numbers are navigation hints. See CONFIGURATION.md for environment variables and DESIGN_CONTROLS.md for Design field units/bounds.

## backend/app/config.py

Backend settings and their validated defaults.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `settings` | React state setter for tings. Schedules a rerender, not a server mutation. | `Settings()` |

### `Settings(BaseSettings)`

Read bounded backend configuration from environment variables and the repository .env file.

Source: [backend/app/config.py:10](../backend/app/config.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / '.env', extra='ignore')` |
| `ffmpeg` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'ffmpeg'` |
| `ffprobe` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'ffprobe'` |
| `node` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'node'` |
| `transcription_cache` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path.home() / '.cache' / 'easypodcast' / 'models'` |
| `transcription_allow_download` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |
| `openai_api_key` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `''` |
| `image_model` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `''` |
| `image_size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'1536x1024'` |
| `image_quality` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'medium'` |
| `temp_root` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path(tempfile.gettempdir()) / 'easypodcast'` |
| `max_audio_bytes` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(1024 ** 3, gt=0)` |
| `max_srt_bytes` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(5 * 1024 ** 2, gt=0)` |
| `max_image_bytes` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(20 * 1024 ** 2, gt=0)` |
| `max_pixels` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(25000000, gt=0)` |
| `max_duration` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(7200, gt=0)` |
| `ttl_seconds` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(86400, gt=0)` |
| `failure_ttl_seconds` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(900, gt=0)` |
| `active_ttl_seconds` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(14400, gt=0)` |
| `queue_size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(2, ge=1, le=8)` |
| `max_jobs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(8, ge=1, le=100)` |
| `min_free_bytes` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(512 * 1024 ** 2, ge=0)` |
| `allowed_origins` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `['http://127.0.0.1:5173', 'http://localhost:5173', 'http://127.0.0.1:8000', 'http://localhost:8000']` |

## backend/app/fonts.py

Bundled font allowlist and logo coordinate helpers.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `key` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS.items()` |
| `_` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS.items()` |
| `filename` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS.items()` |
| `FONT_DIR` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path(__file__).resolve().parents[2] / 'assets' / 'fonts'` |
| `FONTS` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'sans': ('DejaVu Sans', 'DejaVuSans.ttf'), 'serif': ('DejaVu Serif', 'DejaVuSerif.ttf'), 'mono': ('DejaVu Sans Mono', 'DejaVuSansMono.ttf'), 'nunito': ('Nunito', 'Nunito-Regular.ttf'), 'fredoka': ('F` |
| `BOLD_FILES` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'sans': 'DejaVuSans-Bold.ttf', 'serif': 'DejaVuSerif-Bold.ttf', 'mono': 'DejaVuSansMono-Bold.ttf', **{key: filename.replace('-Regular.ttf', '-Bold.ttf') for key, (_, filename) in FONTS.items() if key` |

### `font_path(key, bold=False)`

Resolve an allowlisted font key and weight to a bundled font file.

Source: [backend/app/fonts.py:33](../backend/app/fonts.py).

- `key`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `bold`: Whether to select the actual Bold font/style.

### `logo_position(design)`

Convert a validated logo placement into FFmpeg overlay coordinate expressions.

Source: [backend/app/fonts.py:38](../backend/app/fonts.py).

- `design`: Validated episode appearance/encoding settings or unsaved browser draft.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `margin` | Canvas inset measured in video pixels. | `design.logo_margin` |
| `x` | Horizontal title coordinate in video pixels, when used in make_ass. | `'W-w-' + str(margin) if design.logo_position.endswith('right') else str(margin)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `str(margin)` |

## backend/app/images.py

Optional paid image-provider boundary; never used implicitly.

### `ImageProvider(Protocol)`

Describe the background-generation contract used by real and fake providers.

Source: [backend/app/images.py:13](../backend/app/images.py).

### `ImageProvider.generate_background(self, design, destination: Path)`

Write a normalized background image at destination; raise a sanitized error on failure.

Source: [backend/app/images.py:16](../backend/app/images.py).

- `self`: The current Python class instance.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `destination`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `OpenAIProvider()`

Generate one explicitly requested image without automatically retrying billable calls.

Source: [backend/app/images.py:21](../backend/app/images.py).

### `OpenAIProvider.generate_background(self, design, destination: Path)`

Write a normalized background image at destination; raise a sanitized error on failure.

Source: [backend/app/images.py:24](../backend/app/images.py).

- `self`: The current Python class instance.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `destination`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `prompt` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'Horizontal podcast studio background, two fictional adult hosts, woman on the left, man on the right, microphones. Leave central space and lower third clear. No text, logos, lettering or waveforms. ` |
| `result` | Result of the operation/parser/API named by its assignment. | `client.images.generate(model=settings.image_model, prompt=prompt, n=1, size=settings.image_size, quality=settings.image_quality)` |
| `encoded` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `result.data[0].b64_json` |
| `raw` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `destination.with_suffix('.raw')` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |
| `messages` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{401: 'Clave del proveedor inválida.', 403: 'Acceso al modelo no autorizado.', 429: 'Cuota o límite del proveedor alcanzado.'}` |

## backend/app/jobs.py

Temporary job lifecycle, one worker, cancellation and safe cleanup.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `ACTIVE` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'queued', 'transcribing', 'generating_image', 'rendering_preview', 'rendering_video', 'cancelling'}` |
| `store` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Store()` |

### `Job()`

Hold one temporary episode, its files, state, approvals and cancellation resources.

Source: [backend/app/jobs.py:24](../backend/app/jobs.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `id` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `annotation / loop binding` |
| `token` | Secret authentication value held in memory and sent in X-Job-Token. | `annotation / loop binding` |
| `path` | Controlled filesystem location, never an uploaded filename. | `annotation / loop binding` |
| `meta` | Inspected audio metadata including duration and selected stream. | `annotation / loop binding` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `annotation / loop binding` |
| `warnings` | Nonfatal review messages such as overlap or estimated timing. | `annotation / loop binding` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `field(default_factory=Design)` |
| `state` | Lifecycle enum, independent of interface language. | `'ready'` |
| `phase` | Human-readable description of the current operation. | `'Listo para diseñar'` |
| `progress` | Processed fraction from 0 to 1, or None/null for indeterminate work. | `None` |
| `error` | Safe explanatory failure text; must not expose secrets or raw stderr. | `None` |
| `expires` | Idle expiry in Unix seconds; polling must not extend it. | `field(default_factory=lambda: time.time() + settings.ttl_seconds)` |
| `active_deadline` | Absolute Unix deadline for an active operation. | `0` |
| `approved` | Whether the current background was explicitly reviewed. | `False` |
| `preview_approved` | Whether the current preview was explicitly reviewed. | `False` |
| `artifacts` | Available output kinds; stale renders are discarded after edits. | `field(default_factory=lambda: {'background'})` |
| `background_mode` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'local'` |
| `cancel` | Backend cancellation event or frontend operation name, according to scope. | `field(default_factory=threading.Event)` |
| `process` | Supervised child process; stop it before releasing the worker. | `None` |
| `readers` | Active download leases that prevent premature cleanup. | `0` |
| `deleting` | Deferred deletion flag; cleanup waits for readers/workers. | `False` |
| `subtitle_source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'upload'` |
| `subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |
| `transcription_options` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `field(default_factory=TranscriptionOptions)` |

### `Job.public(self)`

Return the token-free job snapshot exposed by status polling.

Source: [backend/app/jobs.py:52](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `self.cues` |

### `Store()`

Own the in-memory registry, locks, bounded queue, worker and managed cleanup.

Source: [backend/app/jobs.py:77](../backend/app/jobs.py).

### `Store.__init__(self)`

Initialize the instance resources; background threads are started separately.

Source: [backend/app/jobs.py:80](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `self.jobs` | In-memory registry indexed by random job ID; lost on restart. | `{}` |
| `self.lock` | Reentrant lock protecting shared registry changes. | `threading.RLock()` |
| `self.queue` | Bounded FIFO of pending operations consumed by one worker. | `queue.Queue(maxsize=settings.queue_size)` |
| `self.stop` | Shutdown event checked by worker and cleanup loops. | `threading.Event()` |
| `self.root` | Exclusive temporary root or repository root; inspect the initializer. | `settings.temp_root.resolve()` |
| `self.provider` | Image provider; tests replace it with a fake to avoid charges. | `OpenAIProvider()` |

### `Store.start(self)`

Lock the exclusive temporary root, remove stale managed jobs and start worker/cleaner threads.

Source: [backend/app/jobs.py:89](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `path.name` |
| `marker` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `self.root / '.easypodcast-root'` |
| `self.file_lock` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FileLock(str(self.root / '.instance.lock'))` |
| `path` | Controlled filesystem location, never an uploaded filename. | `self.root.iterdir()` |
| `self.worker` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=self.work, daemon=True)` |
| `self.cleaner` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=self.clean_loop, daemon=True)` |

### `Store.close(self)`

Request cancellation, join background threads and release managed resources and the root lock.

Source: [backend/app/jobs.py:108](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `self.jobs.values()` |

### `Store.remove_path(self, path)`

Remove only a direct managed child, without following a symbolic link.

Source: [backend/app/jobs.py:122](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `path`: Controlled filesystem location, never an uploaded filename.

### `Store.new_path(self)`

Create a UUID-named directory and return its ID and path.

Source: [backend/app/jobs.py:131](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `jid` | Random public job ID; a separate secret token is required. | `uuid.uuid4().hex` |
| `path` | Controlled filesystem location, never an uploaded filename. | `self.root / jid` |

### `Store.enqueue(self, job, kind, start=0)`

Queue a copied Design snapshot after checking busy and queue-capacity constraints.

Source: [backend/app/jobs.py:138](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.
- `kind`: Allowlisted operation/artifact key, not an arbitrary filename.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('queued', 'En cola', None)` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('queued', 'En cola', None)` |
| `job.error` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('queued', 'En cola', None)` |
| `job.progress` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |
| `job.active_deadline` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time() + settings.active_ttl_seconds` |

### `Store.invalidate(self, job)`

Discard preview/video artifacts and clear approval after a design or input change.

Source: [backend/app/jobs.py:151](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `kind` | Allowlisted operation/artifact key, not an arbitrary filename. | `('preview', 'video')` |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |

### `Store.work(self)`

Consume queued operations serially, publish validated artifacts and update retention/state.

Source: [backend/app/jobs.py:158](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `jid` | Random public job ID; a separate secret token is required. | `self.queue.get(timeout=0.3)` |
| `kind` | Allowlisted operation/artifact key, not an arbitrary filename. | `self.queue.get(timeout=0.3)` |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `self.queue.get(timeout=0.3)` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `self.queue.get(timeout=0.3)` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `self.jobs.get(jid)` |
| `output` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.path / ('generated.png' if kind == 'background' else f'{kind}.partial.mp4')` |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'transcript': 'transcribing', 'background': 'generating_image', 'preview': 'rendering_preview', 'video': 'rendering_video'}[kind]` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'transcript': 'Transcribiendo audio localmente', 'background': 'Generando imagen', 'preview': 'Renderizando prueba', 'video': 'Renderizando episodio'}[kind]` |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `transcribe(job)` |
| `srt` | SRT under review; editing intentionally discards word alignment. | `transcribe(job)` |
| `duration` | Audio or clip length in seconds. | `min(20, job.meta['duration'] - start) if kind == 'preview' else job.meta['duration']` |
| `job.cues` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues` |
| `job.warnings` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `['Transcripción automática: revisa texto y tiempos estimados antes de continuar.']` |
| `job.background_mode` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('openai', False)` |
| `job.approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('openai', False)` |
| `job.progress` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None if kind == 'background' else 1.0` |
| `job.expires` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time() + settings.ttl_seconds` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |
| `job.error` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `str(exc) if isinstance(exc, ValueError) else 'Error interno al procesar el trabajo.'` |

### `Store.clean_loop(self)`

Periodically request cleanup until shutdown is signalled.

Source: [backend/app/jobs.py:244](../backend/app/jobs.py).

- `self`: The current Python class instance.

### `Store.cleanup(self)`

Cancel overdue active jobs and remove expired/deleted idle jobs without active readers.

Source: [backend/app/jobs.py:249](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `now` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time()` |
| `jid` | Random public job ID; a separate secret token is required. | `list(self.jobs.items())` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `list(self.jobs.items())` |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'cancelling'` |

### `make_job(jid, path, meta, cues, warnings)`

Construct a temporary job with a random token and initial validated metadata.

Source: [backend/app/jobs.py:266](../backend/app/jobs.py).

- `jid`: Random public job ID; a separate secret token is required.
- `path`: Controlled filesystem location, never an uploaded filename.
- `meta`: Inspected audio metadata including duration and selected stream.
- `cues`: Ordered subtitle intervals with optional estimated word timing.
- `warnings`: Nonfatal review messages such as overlap or estimated timing.

## backend/app/main.py

FastAPI endpoints, local request guards and authenticated artifact responses.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `app` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FastAPI(title='EasyPodcast', version='0.4.1', lifespan=lifespan)` |
| `frontend` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ROOT / 'frontend' / 'dist'` |

### `lifespan(app)`

Start the store and compute capabilities at startup; close resources during shutdown.

Source: [backend/app/main.py:24](../backend/app/main.py).

- `app`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `app.state.upload_slot` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `asyncio.Semaphore(1)` |
| `app.state.capabilities` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await asyncio.to_thread(capabilities)` |

### `RequestGuard()`

Enforce allowed browser origins and a total request-body byte budget.

Source: [backend/app/main.py:37](../backend/app/main.py).

### `RequestGuard.__init__(self, app)`

Initialize the instance resources; background threads are started separately.

Source: [backend/app/main.py:40](../backend/app/main.py).

- `self`: The current Python class instance.
- `app`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `self.app` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `app` |

### `RequestGuard.__call__(self, scope, receive, send)`

Handle an ASGI request while preserving middleware or response cleanup guarantees.

Source: [backend/app/main.py:44](../backend/app/main.py).

- `self`: The current Python class instance.
- `scope`: ASGI context with path, headers and protocol metadata.
- `receive`: ASGI callable reading incoming body events.
- `send`: ASGI callable sending outgoing response events.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `headers` | HTTP headers, including origin or authentication as needed. | `dict(scope['headers'])` |
| `origin` | Browser origin checked against the local allowlist. | `headers.get(b'origin', b'').decode()` |
| `method` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `scope['method']` |
| `total` | Accumulated incoming body bytes. | `0` |
| `limit` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `settings.max_audio_bytes + settings.max_srt_bytes + settings.max_image_bytes * 2 + 1024 ** 2` |

### `RequestGuard.__call__.bounded_receive()`

Count streamed ASGI body bytes and enforce the total upload budget.

Source: [backend/app/main.py:58](../backend/app/main.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `message` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await receive()` |
| `total` | Accumulated incoming body bytes. | `len(message.get('body', b''))` |

### `invalid(request, exc)`

Convert a validation ValueError into a safe HTTP 422 response.

Source: [backend/app/main.py:74](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `exc`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `health()`

Expose service liveness and version without secrets.

Source: [backend/app/main.py:80](../backend/app/main.py).


### `get_capabilities(request: Request)`

Return dependency and limit checks computed at application startup.

Source: [backend/app/main.py:86](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.

### `get_job(jid: str, request: Request)`

Authenticate the job token and reject absent, expired or invalid sessions.

Source: [backend/app/main.py:91](../backend/app/main.py).

- `jid`: Random public job ID; a separate secret token is required.
- `request`: HTTP request containing headers and a streamed body.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `store.jobs.get(jid)` |
| `token` | Secret authentication value held in memory and sent in X-Job-Token. | `request.headers.get('X-Job-Token', '')` |

### `editable(job)`

Reject edits while an operation or artifact download holds the job.

Source: [backend/app/main.py:111](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `create_job(request: Request, subtitle_mode: Literal['upload', 'generate']='upload', language: Literal['auto', 'en', 'es', 'pt', 'fr', 'de', 'it']='en', model: Literal['tiny', 'base']='tiny')`

Serialize uploads and dispatch creation for the selected subtitle source.

Source: [backend/app/main.py:138](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `subtitle_mode`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `language`: Spoken audio language sent to Whisper, not interface locale.
- `model`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `['audio', 'srt', 'image', 'logo']` |

### `create_uploaded_job(request, subtitle_mode, options)`

Receive and validate uploads, create an episode and optionally queue local transcription.

Source: [backend/app/main.py:153](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `subtitle_mode`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `options`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues` |
| `jid` | Random public job ID; a separate secret token is required. | `store.new_path()` |
| `path` | Controlled filesystem location, never an uploaded filename. | `store.new_path()` |
| `files` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await receive_files(request, path, require_srt=subtitle_mode == 'upload')` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |
| `meta` | Inspected audio metadata including duration and selected stream. | `await asyncio.to_thread(validate_audio, path / 'audio.bin')` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `parse_srt((path / 'original.srt').read_bytes()) if subtitle_mode == 'upload' else ([], [])` |
| `warnings` | Nonfatal review messages such as overlap or estimated timing. | `parse_srt((path / 'original.srt').read_bytes()) if subtitle_mode == 'upload' else ([], [])` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `make_job(jid, path, meta, cues, warnings)` |
| `job.subtitle_source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `subtitle_mode` |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `subtitle_mode == 'upload'` |
| `job.transcription_options` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `options` |
| `job.background_mode` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'upload' if 'image' in files else 'local'` |
| `response` | Outgoing HTTP response or inspected fetch result. | `JSONResponse({**job.public(), 'token': job.token}, status_code=201)` |

### `status(response: Response, job=Depends(get_job))`

Return a job snapshot and refresh the media cookie only to its existing expiry.

Source: [backend/app/main.py:226](../backend/app/main.py).

- `response`: Outgoing HTTP response or inspected fetch result.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `deadline` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.active_deadline + settings.ttl_seconds if job.state in ACTIVE else job.expires` |

### `configure(design: Design, job=Depends(get_job))`

Replace validated Design settings and invalidate previous approvals/artifacts.

Source: [backend/app/main.py:243](../backend/app/main.py).

- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.design` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design` |

### `generate(job=Depends(get_job))`

Queue explicit optional provider generation for the current job.

Source: [backend/app/main.py:253](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `approve_background(job=Depends(get_job))`

Mark the current background reviewed without generating or rendering anything.

Source: [backend/app/main.py:262](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `approve_preview(job=Depends(get_job))`

Mark the current preview reviewed after checking that it exists.

Source: [backend/app/main.py:271](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `check_render(job)`

Enforce dependencies, subtitle/background approval, trim permission and disk budget.

Source: [backend/app/main.py:281](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `required` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `settings.min_free_bytes + int(job.meta['duration'] * 1000000)` |

### `preview(body: PreviewRequest, job=Depends(get_job))`

Queue up to 20 seconds from the validated starting offset.

Source: [backend/app/main.py:298](../backend/app/main.py).

- `body`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `export(job=Depends(get_job))`

Queue full-episode export only after the current preview has been approved.

Source: [backend/app/main.py:310](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `cancel(job=Depends(get_job))`

Signal cancellation and expose a cancelling phase without blocking the API.

Source: [backend/app/main.py:322](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('cancelling', 'Cancelando operación')` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('cancelling', 'Cancelando operación')` |

### `delete(job=Depends(get_job))`

Request cancellation and deferred deletion of this managed episode.

Source: [backend/app/main.py:332](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.deleting` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `artifact(kind: str, download: bool=False, job=Depends(get_job))`

Serve an allowlisted artifact, holding a reader lease for media streaming.

Source: [backend/app/main.py:342](../backend/app/main.py).

- `kind`: Allowlisted operation/artifact key, not an arbitrary filename.
- `download`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `mapping` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'logo': ('logo.png', 'image/png'), 'subtitles': ('generated.srt' if job.subtitle_source == 'generate' else 'original.srt', 'application/x-subrip'), 'background': ('background.png', 'image/png'), 'pre` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `mapping[kind]` |
| `mime` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `mapping[kind]` |
| `job.readers` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1` |

### `artifact.release()`

Release one download reader and retry deferred cleanup.

Source: [backend/app/main.py:370](../backend/app/main.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.readers` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1` |

### `artifact.LeasedFileResponse(FileResponse)`

Release a download reader lease even when response streaming fails or disconnects.

Source: [backend/app/main.py:376](../backend/app/main.py).

### `artifact.LeasedFileResponse.__call__(self, scope, receive, send)`

Handle an ASGI request while preserving middleware or response cleanup guarantees.

Source: [backend/app/main.py:379](../backend/app/main.py).

- `self`: The current Python class instance.
- `scope`: ASGI context with path, headers and protocol metadata.
- `receive`: ASGI callable reading incoming body events.
- `send`: ASGI callable sending outgoing response events.

### `retry_transcription(job=Depends(get_job))`

Queue transcription again only for episodes created in generate mode.

Source: [backend/app/main.py:395](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `subtitles(job=Depends(get_job))`

Read the reviewable SRT and expose whether word timestamps exist.

Source: [backend/app/main.py:404](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `path` | Controlled filesystem location, never an uploaded filename. | `job.path / ('generated.srt' if job.subtitle_source == 'generate' else 'original.srt')` |

### `edit_subtitles(body: SubtitleEdit, job=Depends(get_job))`

Validate edited SRT, drop stale word timing and invalidate previous renders.

Source: [backend/app/main.py:419](../backend/app/main.py).

- `body`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `parse_srt(body.srt.encode())` |
| `warnings` | Nonfatal review messages such as overlap or estimated timing. | `parse_srt(body.srt.encode())` |
| `path` | Controlled filesystem location, never an uploaded filename. | `job.path / ('generated.srt' if job.subtitle_source == 'generate' else 'original.srt')` |
| `job.cues` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues` |
| `job.warnings` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `warnings + ['SRT editado: se desactiva resaltado por palabra para no usar tiempos desactualizados.']` |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |

### `approve_subtitles(job=Depends(get_job))`

Approve generated or edited cues so the user can proceed to design.

Source: [backend/app/main.py:441](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `font_file(key: str, bold: bool=False)`

Serve an allowlisted bundled font and reject arbitrary path requests.

Source: [backend/app/main.py:452](../backend/app/main.py).

- `key`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `bold`: Whether to select the actual Bold font/style.

## backend/app/media.py

Native media inspection, image normalization and supervised FFmpeg rendering.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `ROOT` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path(__file__).resolve().parents[2]` |

### `run(args, timeout=30)`

Run a short command with checked exit status, captured UTF-8 output and a timeout.

Source: [backend/app/media.py:22](../backend/app/media.py).

- `args`: Checked subprocess arguments or parsed CLI options, according to scope.
- `timeout`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `capabilities()`

Inspect executables, filters, encoders, fonts, transcription installation and limits.

Source: [backend/app/media.py:36](../backend/app/media.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `key` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS` |
| `bold` | Whether to select the actual Bold font/style. | `(False, True)` |
| `value` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS.items()` |
| `f` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('ass', 'showwaves', 'showfreqs', 'colorkey', 'overlay')` |
| `result` | Result of the operation/parser/API named by its assignment. | `{'ffmpeg': bool(shutil.which(settings.ffmpeg)), 'ffprobe': bool(shutil.which(settings.ffprobe)), 'filters': {}, 'h264': False, 'aac': False, 'font': all((font_path(key, bold).is_file() for key in FONT` |
| `filters` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `run([settings.ffmpeg, '-hide_banner', '-filters']).stdout` |
| `encoders` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `run([settings.ffmpeg, '-hide_banner', '-encoders']).stdout` |

### `probe(path: Path)`

Read actual media streams and duration using FFprobe JSON output.

Source: [backend/app/media.py:96](../backend/app/media.py).

- `path`: Controlled filesystem location, never an uploaded filename.

### `validate_audio(path: Path)`

Reject unsupported or excessive audio and return the selected stream metadata.

Source: [backend/app/media.py:118](../backend/app/media.py).

- `path`: Controlled filesystem location, never an uploaded filename.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `s` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `meta['streams']` |
| `meta` | Inspected audio metadata including duration and selected stream. | `probe(path)` |
| `streams` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[s for s in meta['streams'] if s['codec_type'] == 'audio']` |
| `duration` | Audio or clip length in seconds. | `float(meta['format']['duration'])` |
| `formats` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `set(meta['format']['format_name'].split(','))` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |

### `normalize_image(source: Path, target: Path, logo=False)`

Decode and size-bound an uploaded image before producing a normalized PNG.

Source: [backend/app/media.py:139](../backend/app/media.py).

- `source`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `target`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `logo`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `image` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageOps.exif_transpose(im).convert('RGBA' if logo else 'RGB')` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |

### `local_background(target: Path)`

Draw the deterministic local demonstration background without an external service.

Source: [backend/app/media.py:159](../backend/app/media.py).

- `target`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `image` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Image.new('RGB', (1920, 1080), '#101522')` |
| `draw` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageDraw.Draw(image)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `range(1080)` |

### `terminate(process)`

Stop the subprocess tree/group and wait for it to exit on Windows or POSIX.

Source: [backend/app/media.py:171](../backend/app/media.py).

- `process`: Supervised child process; stop it before releasing the worker.

### `render(job, design, start, duration, output, update)`

Build ASS/filtergraph inputs, supervise FFmpeg and validate the finished MP4 before publication.

Source: [backend/app/media.py:188](../backend/app/media.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.
- `duration`: Audio or clip length in seconds.
- `output`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `update`: Callback reporting real render progress.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `s` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `result['streams']` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `clip_cues(job.cues, start, duration)` |
| `fonts` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.path / 'fonts'` |
| `key` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FONTS` |
| `bold` | Whether to select the actual Bold font/style. | `(False, True)` |
| `source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `font_path(key, bold)` |
| `size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'1600x{round(1080 * design.wave_height) // 2 * 2}'` |
| `color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'0x' + design.color[1:]` |
| `visual` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'showwaves=s={size}:mode=line:rate=30:colors={color}' if design.visualizer == 'waveform' else f'showfreqs=s={size}:mode=bar:ascale=sqrt:fscale=log:colors={color}:rate=30'` |
| `graph` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f"[1:{job.meta['audio_stream']}]asplit=2[aout][viz];[viz]volume={design.sensitivity},{visual},format=rgba,colorkey=0x000000:0.03:0.0[wave];[0:v][wave]overlay=160:{round(1080 * design.wave_y)}:shortest` |
| `inputs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[settings.ffmpeg, '-hide_banner', '-nostdin', '-y', '-loop', '1', '-framerate', '30', '-i', 'background.png', '-ss', str(start), '-i', 'audio.bin']` |
| `x` | Horizontal title coordinate in video pixels, when used in make_ass. | `logo_position(design)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `logo_position(design)` |
| `args` | Checked subprocess arguments or parsed CLI options, according to scope. | `inputs + ['-filter_complex', graph, '-map', '[v]', '-map', '[aout]', '-t', str(duration), '-r', '30', '-c:v', 'libx264', '-preset', design.preset, '-crf', str(design.crf), '-c:a', 'aac', '-b:a', '192k` |
| `logs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `deque(maxlen=40)` |
| `process` | Supervised child process; stop it before releasing the worker. | `subprocess.Popen(args, cwd=job.path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace', shell=False, start_new_session=os.name != 'nt')` |
| `job.process` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process` |
| `readers` | Active download leases that prevent premature cleanup. | `[threading.Thread(target=read_progress, daemon=True), threading.Thread(target=read_errors, daemon=True)]` |
| `reader` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `readers` |
| `result` | Result of the operation/parser/API named by its assignment. | `probe(output)` |
| `videos` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[s for s in result['streams'] if s['codec_type'] == 'video']` |
| `audios` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[s for s in result['streams'] if s['codec_type'] == 'audio']` |
| `v` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `videos[0]` |

### `render.read_progress()`

Drain FFmpeg progress lines without blocking the rendering supervisor.

Source: [backend/app/media.py:282](../backend/app/media.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.stdout` |

### `render.read_errors()`

Drain bounded FFmpeg error output so a full stderr pipe cannot deadlock rendering.

Source: [backend/app/media.py:291](../backend/app/media.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.stderr` |

## backend/app/models.py

Pydantic request contracts; UI types alone are not server validation.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `FontKey` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Literal['sans', 'serif', 'mono', 'nunito', 'fredoka', 'quicksand', 'poppins', 'baloo2', 'outfit', 'balsamiqsans', 'lexend', 'atkinsonhyperlegible', 'comicneue']` |

### `Design(BaseModel)`

Validate the complete episode appearance and encoding settings at the API boundary.

Source: [backend/app/models.py:24](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid', allow_inf_nan=False)` |
| `title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('My episode', max_length=120)` |
| `description` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('', max_length=1200)` |
| `image_style` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'illustration'` |
| `atmosphere` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('Cozy studio, blue and coral', max_length=300)` |
| `visualizer` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'waveform'` |
| `color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('#5EEAD4', pattern='^#[0-9a-fA-F]{6}$')` |
| `sensitivity` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(1, ge=0.2, le=4)` |
| `wave_y` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(0.52, ge=0.3, le=0.65)` |
| `wave_height` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(0.16, ge=0.06, le=0.22)` |
| `font_size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(48, ge=28, le=72)` |
| `subtitle_font` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'sans'` |
| `title_font` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'sans'` |
| `title_bold` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |
| `title_font_size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(64, ge=28, le=110)` |
| `title_offset_x` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(0, ge=-600, le=600)` |
| `title_offset_y` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(0, ge=-80, le=400)` |
| `logo_position` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'top-right'` |
| `logo_margin` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(40, ge=20, le=160)` |
| `subtitle_color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('#FFFFFF', pattern='^#[0-9a-fA-F]{6}$')` |
| `outline` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(3, ge=1, le=6)` |
| `subtitle_margin` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(80, ge=40, le=180)` |
| `subtitle_width` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(0.85, ge=0.5, le=0.9)` |
| `max_lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(2, ge=2, le=3)` |
| `crf` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(21, ge=18, le=28)` |
| `preset` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'veryfast'` |
| `trim_subtitles` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |
| `highlight_words` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |
| `highlight_color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field('#FFD54A', pattern='^#[0-9a-fA-F]{6}$')` |

### `Design.safe_layout(self)`

Reject subtitle and visualizer overlap using canvas-coordinate layout estimates.

Source: [backend/app/models.py:88](../backend/app/models.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `subtitle_top` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1080 - self.subtitle_margin - self.font_size * self.max_lines * 1.25 - 20` |

### `PreviewRequest(BaseModel)`

Validate the nonnegative preview start time in seconds.

Source: [backend/app/models.py:96](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid', allow_inf_nan=False)` |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `Field(0, ge=0)` |

### `TranscriptionOptions(BaseModel)`

Allowlist the local Whisper model and spoken audio language.

Source: [backend/app/models.py:104](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `language` | Spoken audio language sent to Whisper, not interface locale. | `'en'` |
| `model` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'tiny'` |

### `SubtitleEdit(BaseModel)`

Bound the size of an edited SRT payload.

Source: [backend/app/models.py:114](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `srt` | SRT under review; editing intentionally discards word alignment. | `Field(min_length=1, max_length=5 * 1024 ** 2)` |

## backend/app/subtitles.py

SRT/ASS timing, wrapping, escaping and estimated current-word highlighting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `TIME` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'(\\d{2,}):([0-5]\\d):([0-5]\\d)[,.](\\d{3})'` |
| `TIMING` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `re.compile(f'^{TIME}\\s+-->\\s+{TIME}\\s*$')` |

### `Word(BaseModel)`

Validate one recognized word with start/end times in seconds.

Source: [backend/app/subtitles.py:12](../backend/app/subtitles.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid', allow_inf_nan=False)` |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `Field(ge=0)` |
| `end` | Interval end in seconds; in multipart callbacks, byte-slice end index. | `Field(gt=0)` |
| `text` | Subtitle/title text; escape before ASS insertion and never translate user content. | `Field(min_length=1, max_length=200)` |

### `Word.valid_interval(self)`

Require visible word text and an end time strictly after the start.

Source: [backend/app/subtitles.py:21](../backend/app/subtitles.py).

- `self`: The current Python class instance.

### `Cue()`

Represent one subtitle interval and optional word timing needed for highlighting.

Source: [backend/app/subtitles.py:29](../backend/app/subtitles.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `annotation / loop binding` |
| `end` | Interval end in seconds; in multipart callbacks, byte-slice end index. | `annotation / loop binding` |
| `text` | Subtitle/title text; escape before ASS insertion and never translate user content. | `annotation / loop binding` |
| `words` | Validated recognized word intervals used for grouping/highlighting. | `()` |
| `word_offset` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |

### `parse_srt(data: bytes)`

Decode UTF-8 SRT, validate ordered intervals and return cues plus review warnings.

Source: [backend/app/subtitles.py:43](../backend/app/subtitles.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `text` |
| `content` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `data.decode('utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').strip()` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `([], [])` |
| `warnings` | Nonfatal review messages such as overlap or estimated timing. | `([], [])` |
| `block` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `re.split('\\n\\s*\\n', content)` |
| `lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `block.splitlines()` |
| `match` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `TIMING.fullmatch(lines[0].strip()) if lines else None` |
| `n` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `list(map(int, match.groups()))` |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `n[0] * 3600 + n[1] * 60 + n[2] + n[3] / 1000` |
| `end` | Interval end in seconds; in multipart callbacks, byte-slice end index. | `n[4] * 3600 + n[5] * 60 + n[6] + n[7] / 1000` |
| `text` | Subtitle/title text; escape before ASS insertion and never translate user content. | `html.unescape(re.sub('<[^>]*>', '', '\n'.join(lines[1:])))` |

### `clip_cues(cues: list[Cue], start: float, duration: float)`

Intersect cues/words with the preview interval and shift timing to the new zero point.

Source: [backend/app/subtitles.py:78](../backend/app/subtitles.py).

- `cues`: Ordered subtitle intervals with optional estimated word timing.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.
- `duration`: Audio or clip length in seconds.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `c.words` |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues` |

### `escape_ass(text: str)`

Escape literal user text so ASS override syntax cannot be injected.

Source: [backend/app/subtitles.py:97](../backend/app/subtitles.py).

- `text`: Subtitle/title text; escape before ASS insertion and never translate user content.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `text` |
| `text` | Subtitle/title text; escape before ASS insertion and never translate user content. | `''.join((c for c in text if c == '\n' or ord(c) >= 32))` |

### `wrap_text(text, font_key, size, width, bold=False)`

Measure the selected real font and split text into lines within the pixel width.

Source: [backend/app/subtitles.py:105](../backend/app/subtitles.py).

- `text`: Subtitle/title text; escape before ASS insertion and never translate user content.
- `font_key`: Allowlisted font ID used for real font measurement.
- `size`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `width`: Available width in video pixels for text wrapping.
- `bold`: Whether to select the actual Bold font/style.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `font` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageFont.truetype(str(font_path(font_key, bold)), size)` |
| `output` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `paragraph` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `text.splitlines()` |
| `remaining` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `paragraph` |
| `count` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1` |
| `split` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `remaining.rfind(' ', 0, count + 1)` |

### `wrap_caption(text, design)`

Wrap subtitle text and reject layouts exceeding the selected line limit.

Source: [backend/app/subtitles.py:126](../backend/app/subtitles.py).

- `text`: Subtitle/title text; escape before ASS insertion and never translate user content.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `output` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `wrap_text(text, design.subtitle_font, design.font_size, 1920 * design.subtitle_width - 40)` |

### `ass_time(seconds: float)`

Format seconds as nonnegative ASS centisecond timestamps.

Source: [backend/app/subtitles.py:136](../backend/app/subtitles.py).

- `seconds`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `cs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `max(0, round(seconds * 100))` |

### `render_srt(cues)`

Serialize cues using numbered UTF-8 SRT blocks and millisecond timestamps.

Source: [backend/app/subtitles.py:142](../backend/app/subtitles.py).

- `cues`: Ordered subtitle intervals with optional estimated word timing.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `i` | Zero-based iteration index local to the current loop. | `enumerate(cues, 1)` |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `enumerate(cues, 1)` |

### `render_srt.stamp(seconds)`

Format seconds as a subtitle timestamp for a generated fixture or SRT.

Source: [backend/app/subtitles.py:145](../backend/app/subtitles.py).

- `seconds`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `ms` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `round(seconds * 1000)` |

### `ass_color(value)`

Convert a validated RGB hex color into ASS BGR notation.

Source: [backend/app/subtitles.py:156](../backend/app/subtitles.py).

- `value`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `value` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `value.lstrip('#')` |

### `highlighted_caption(caption, words, active, design, offset=0)`

Color only the active word while preserving escaped text and clipped offsets.

Source: [backend/app/subtitles.py:162](../backend/app/subtitles.py).

- `caption`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `words`: Validated recognized word intervals used for grouping/highlighting.
- `active`: Whether the job is queued/running/cancelling.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `offset`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `words[:active]` |
| `low` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `offset + sum((len(''.join(w.text.split())) for w in words[:active]))` |
| `high` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `low + len(''.join(words[active].text.split()))` |
| `result` | Result of the operation/parser/API named by its assignment. | `[]` |
| `position` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `colored` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |
| `char` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caption` |
| `want` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `low <= position < high` |

### `make_ass(cues, design, duration: float)`

Build the complete subtitle/title ASS document at 1920 by 1080 resolution.

Source: [backend/app/subtitles.py:181](../backend/app/subtitles.py).

- `cues`: Ordered subtitle intervals with optional estimated word timing.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `duration`: Audio or clip length in seconds.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cue.words` |
| `t` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(w.start, w.end)` |
| `i` | Zero-based iteration index local to the current loop. | `enumerate(cue.words)` |
| `color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.subtitle_color.lstrip('#')` |
| `margin` | Canvas inset measured in video pixels. | `round(1920 * (1 - design.subtitle_width) / 2)` |
| `header` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Ital` |
| `events` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `x` | Horizontal title coordinate in video pixels, when used in make_ass. | `(960 + design.title_offset_x, 100 + design.title_offset_y)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `(960 + design.title_offset_x, 100 + design.title_offset_y)` |
| `width` | Available width in video pixels for text wrapping. | `min(1600, 2 * (min(x, 1920 - x) - 120))` |
| `lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `wrap_text(design.title, design.title_font, design.title_font_size, width, design.title_bold)` |
| `title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'\n'.join(lines)` |
| `position` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'{{\\an8\\pos({x},{y})}}'` |
| `cue` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues` |
| `caption` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `wrap_caption(cue.text, design)` |
| `boundaries` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sorted({cue.start, cue.end, *[max(cue.start, min(cue.end, t)) for w in cue.words for t in (w.start, w.end)]})` |
| `begin` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `zip(boundaries, boundaries[1:])` |
| `end` | Interval end in seconds; in multipart callbacks, byte-slice end index. | `zip(boundaries, boundaries[1:])` |
| `middle` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(begin + end) / 2` |
| `active` | Whether the job is queued/running/cancelling. | `next((i for i, w in enumerate(cue.words) if w.start <= middle < w.end), None)` |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `highlighted_caption(caption, cue.words, active, design, cue.word_offset) if design.highlight_words and active is not None else escape_ass(caption)` |

## backend/app/transcription.py

Isolated local Whisper inference. Never sends source audio to a service.

### `available()`

Check the Node executable and installed local inference package without downloading models.

Source: [backend/app/transcription.py:15](../backend/app/transcription.py).


### `supervise(job, args, on_event=None)`

Run FFmpeg or Node while monitoring cancellation, timeout, disk space and JSON progress.

Source: [backend/app/transcription.py:23](../backend/app/transcription.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.
- `args`: Checked subprocess arguments or parsed CLI options, according to scope.
- `on_event`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `process` | Supervised child process; stop it before releasing the worker. | `subprocess.Popen(args, cwd=job.path, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding='utf-8', errors='replace', shell=False, start_new_session=os.name != 'nt')` |
| `job.process` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process` |
| `reader` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=read, daemon=True)` |

### `supervise.read()`

Drain child-process JSON events and ignore malformed or oversized event lines.

Source: [backend/app/transcription.py:38](../backend/app/transcription.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.stdout` |

### `transcript_cues(data, duration)`

Validate recognized words and group them into readable subtitle cues.

Source: [backend/app/transcription.py:72](../backend/app/transcription.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.
- `duration`: Audio or clip length in seconds.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `group` |
| `raw` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `data.get('words', [])` |
| `words` | Validated recognized word intervals used for grouping/highlighting. | `[]` |
| `item` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `raw` |
| `word` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Word.model_validate(item)` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `[]` |
| `group` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |

### `transcribe(job)`

Convert audio, run local inference, validate results and remove PCM/JSON intermediates.

Source: [backend/app/transcription.py:100](../backend/app/transcription.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `pcm` | Temporary mono 16 kHz float32 audio for local inference. | `job.path / 'speech.f32'` |
| `result` | Result of the operation/parser/API named by its assignment. | `job.path / 'transcript.partial.json'` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'Preparando audio para transcripción'` |
| `job.progress` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `transcript_cues(json.loads(result.read_text(encoding='utf-8')), job.meta['duration'])` |
| `srt` | SRT under review; editing intentionally discards word alignment. | `render_srt(cues)` |

### `transcribe.event(data)`

Convert worker phase/progress events into safe job status updates.

Source: [backend/app/transcription.py:138](../backend/app/transcription.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'Cargando modelo local (primera vez: descarga de Hugging Face)'` |
| `job.progress` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |
| `processed` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `float(data['processed_seconds'])` |

## backend/app/uploads.py

Bound each multipart file as bytes arrive, before any full-file spooling.

### `receive_files(request, directory, require_srt=True)`

Stream multipart files to controlled names while enforcing per-part and disk limits.

Source: [backend/app/uploads.py:12](../backend/app/uploads.py).

- `request`: HTTP request containing headers and a streamed body.
- `directory`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `require_srt`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `media_type` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_options_header(request.headers.get('content-type', ''))` |
| `options` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_options_header(request.headers.get('content-type', ''))` |
| `boundary` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `options.get(b'boundary')` |
| `limits` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'audio': settings.max_audio_bytes, 'srt': settings.max_srt_bytes, 'image': settings.max_image_bytes, 'logo': settings.max_image_bytes}` |
| `names` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'audio': 'audio.bin', 'srt': 'original.srt', 'image': 'image.bin', 'logo': 'logo.bin'}` |
| `seen` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `set()` |
| `current` | Async cleanup guard against stale/unmounted SRT updates. | `{'file': None, 'name': None, 'size': 0, 'headers': {}, 'field': b'', 'value': b'', 'header_bytes': 0, 'ended': False}` |
| `parser` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `MultipartParser(boundary, {'on_part_begin': part_begin, 'on_header_field': header_field, 'on_header_value': header_value, 'on_header_end': header_end, 'on_headers_finished': headers_finished, 'on_part` |
| `chunk` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `request.stream()` |
| `required` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'audio', 'srt'} if require_srt else {'audio'}` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |

### `receive_files.part_begin()`

Reset multipart state before a new part begins.

Source: [backend/app/uploads.py:37](../backend/app/uploads.py).


### `receive_files.header_field(data, start, end)`

Accumulate a bounded multipart header-name fragment.

Source: [backend/app/uploads.py:41](../backend/app/uploads.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.
- `end`: Interval end in seconds; in multipart callbacks, byte-slice end index.

### `receive_files.header_value(data, start, end)`

Accumulate a bounded multipart header-value fragment.

Source: [backend/app/uploads.py:48](../backend/app/uploads.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.
- `end`: Interval end in seconds; in multipart callbacks, byte-slice end index.

### `receive_files.header_end()`

Finalize the current multipart header field and value.

Source: [backend/app/uploads.py:55](../backend/app/uploads.py).


### `receive_files.headers_finished()`

Validate part disposition and open its allowlisted destination file.

Source: [backend/app/uploads.py:60](../backend/app/uploads.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `_` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_options_header(current['headers'].get(b'content-disposition', b''))` |
| `opts` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_options_header(current['headers'].get(b'content-disposition', b''))` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `opts.get(b'name', b'').decode('utf-8', errors='replace')` |

### `receive_files.part_data(data, start, end)`

Write a streamed file fragment while enforcing byte and free-space limits.

Source: [backend/app/uploads.py:70](../backend/app/uploads.py).

- `data`: Payload being parsed/transferred; validate before trusting fields.
- `start`: Start time in seconds; in multipart callbacks, byte-slice start index.
- `end`: Interval end in seconds; in multipart callbacks, byte-slice end index.

### `receive_files.part_end()`

Close and validate the current nonempty uploaded file.

Source: [backend/app/uploads.py:79](../backend/app/uploads.py).


### `receive_files.finished()`

Record that the multipart parser reached a complete terminal boundary.

Source: [backend/app/uploads.py:86](../backend/app/uploads.py).


## scripts/benchmark.py

Manual reproducible long synthetic render; requires optional psutil in the venv.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `s` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `samples` |
| `k` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `result.items()` |
| `v` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `result.items()` |
| `parser` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `argparse.ArgumentParser()` |
| `args` | Checked subprocess arguments or parsed CLI options, according to scope. | `parser.parse_args()` |
| `root` | Exclusive temporary root or repository root; inspect the initializer. | `Path(__file__).resolve().parents[1]` |
| `audio` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `args.output / 'demo.wav'` |
| `meta` | Inspected audio metadata including duration and selected stream. | `validate_audio(args.output / 'audio.bin')` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `parse_srt((args.output / 'demo.srt').read_bytes())` |
| `_` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_srt((args.output / 'demo.srt').read_bytes())` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `SimpleNamespace(path=args.output.resolve(), meta=meta, cues=cues, cancel=threading.Event(), process=None, active_deadline=time.time() + settings.active_ttl_seconds)` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `Design(title='EasyPodcast synthetic benchmark', preset=args.preset)` |
| `started` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.monotonic()` |
| `samples` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `done` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Event()` |
| `parent` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `psutil.Process(os.getpid())` |
| `thread` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=monitor, daemon=True)` |
| `elapsed` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.monotonic() - started` |
| `result` | Result of the operation/parser/API named by its assignment. | `{'system': platform.platform(), 'python': platform.python_version(), 'logical_cpus': psutil.cpu_count(), 'preset': args.preset, 'crf': design.crf, 'audio_seconds': meta['duration'], 'wall_seconds': el` |

### `monitor()`

Sample process-tree RSS/CPU and managed disk until the benchmark finishes.

Source: [scripts/benchmark.py:62](../scripts/benchmark.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `p` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `args.output.rglob('*')` |
| `last_print` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `processes` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[parent] + parent.children(recursive=True)` |
| `rss` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `cpu` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `process` | Supervised child process; stop it before releasing the worker. | `processes` |
| `times` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.cpu_times()` |
| `disk` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sum((p.stat().st_size for p in args.output.rglob('*') if p.is_file()))` |

## scripts/build_code_reference.py

Generate a scope-based source reference without reading secrets or runtime media.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `ROOT` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path(__file__).resolve().parents[1]` |
| `ROLES` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'job': 'Temporary episode with metadata, files, approvals and cancellation resources.', 'jobs': 'In-memory registry indexed by random job ID; lost on restart.', 'jid': 'Random public job ID; a separa` |

### `meaning(name)`

Explain a domain variable or a React setter; use source expressions for other locals.

Source: [scripts/build_code_reference.py:95](../scripts/build_code_reference.py).

- `name`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `cell(value)`

Escape source excerpts for a Markdown table.

Source: [scripts/build_code_reference.py:110](../scripts/build_code_reference.py).

- `value`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `python_module(path)`

Inventory Python declarations, parameters and assignments by their lexical scope.

Source: [scripts/build_code_reference.py:115](../scripts/build_code_reference.py).

- `path`: Controlled filesystem location, never an uploaded filename.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `tree` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.parse(path.read_text(encoding='utf-8'))` |
| `relative` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `path.relative_to(ROOT).as_posix()` |
| `lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[f'## {relative}', '', ast.get_docstring(tree) or 'Repository utility module.', '']` |

### `python_module.walk(node, scope='module')`

Render one lexical scope and recursively document nested declarations.

Source: [scripts/build_code_reference.py:121](../scripts/build_code_reference.py).

- `node`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `scope`: ASGI context with path, headers and protocol metadata.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `b` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `node.bases` |
| `scope` | ASGI context with path, headers and protocol metadata. | `node.name if scope == 'module' else scope + '.' + node.name` |
| `signature` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.unparse(node.args) if hasattr(node, 'args') else ', '.join((ast.unparse(b) for b in node.bases))` |
| `arg` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `node.args.posonlyargs + node.args.args + node.args.kwonlyargs` |
| `variables` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `definitions` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `child` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.iter_child_nodes(node)` |
| `seen` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `set()` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sorted(variables, key=lambda x: x[1])` |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sorted(variables, key=lambda x: x[1])` |
| `value` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sorted(variables, key=lambda x: x[1])` |
| `definition` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `definitions` |

### `python_module.walk.visit(item)`

Collect assignments while keeping nested function/class scopes separate.

Source: [scripts/build_code_reference.py:147](../scripts/build_code_reference.py).

- `item`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `targets` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `item.targets if isinstance(item, ast.Assign) else [item.target]` |
| `value` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `getattr(item, 'value', None) or getattr(item, 'iter', None)` |
| `target` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `targets` |
| `sub` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.walk(target)` |
| `child` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.iter_child_nodes(item)` |

### `main()`

Generate docs/CODE_REFERENCE.md from application and utility source, not runtime files.

Source: [scripts/build_code_reference.py:194](../scripts/build_code_reference.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `['# Source code reference', '', 'Generated inventory of application/utility classes, named functions, parameters and assigned variables by lexical scope. Read JUNIOR_GUIDE.md first for a guided walkth` |
| `paths` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sorted((ROOT / 'backend/app').glob('*.py')) + sorted((ROOT / 'scripts').glob('*.py'))` |
| `path` | Controlled filesystem location, never an uploaded filename. | `paths` |
| `result` | Result of the operation/parser/API named by its assignment. | `subprocess.run(['node', str(ROOT / 'scripts/source_symbols.cjs')], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', check=True)` |
| `module` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `json.loads(result.stdout)` |
| `symbol` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `module['symbols']` |
| `explanation` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `symbol['purpose'] or meaning(symbol['name'])` |

## scripts/doctor.py

Run from repository root with its virtualenv Python.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `result` | Result of the operation/parser/API named by its assignment. | `capabilities()` |

## scripts/fixtures.py

Synthetic local silence/tone and SRT; no personal recordings.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `parser` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `argparse.ArgumentParser()` |
| `args` | Checked subprocess arguments or parsed CLI options, according to scope. | `parser.parse_args()` |
| `blocks` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `i` | Zero-based iteration index local to the current loop. | `enumerate(range(0, args.seconds, 4), 1)` |
| `t` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `enumerate(range(0, args.seconds, 4), 1)` |

### `stamp(t)`

Format whole seconds as an SRT millisecond timestamp for synthetic fixtures.

Source: [scripts/fixtures.py:34](../scripts/fixtures.py).

- `t`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

## scripts/render_cli.py

Small local pipeline for debugging; outputs are explicitly retained by the user.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `parser` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `argparse.ArgumentParser()` |
| `args` | Checked subprocess arguments or parsed CLI options, according to scope. | `parser.parse_args()` |
| `meta` | Inspected audio metadata including duration and selected stream. | `validate_audio(args.audio)` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `parse_srt(args.srt.read_bytes())` |
| `_` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parse_srt(args.srt.read_bytes())` |
| `path` | Controlled filesystem location, never an uploaded filename. | `Path(folder)` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `SimpleNamespace(path=path, meta=meta, cues=cues, cancel=threading.Event(), process=None, active_deadline=time.time() + settings.active_ttl_seconds)` |

## frontend/src/api.ts

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.ApiError` | ClassDeclaration | Carry an HTTP status with a safe explanatory error message. | `` |
| `ApiError.callback@5` | Constructor | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ApiError.message` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `ApiError.status` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `module.isActive` | VariableDeclaration | Recognize the server states that prevent conflicting edits. | `(job: Job \| null) => !!job && [ "queued", "transcribing", "generating_image", "rendering_preview", "rendering_video", "cancelling", ].includes(job.state)` |
| `module.callback@14` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job \| null` |
| `module.api` | FunctionDeclaration | Fetch a same-origin API resource with header-token authentication and structured errors. | `path: string, token?: string, method = "GET", body?: BodyInit` |
| `api.path` | Parameter | Controlled filesystem location, never an uploaded filename. | `string` |
| `api.token` | Parameter | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `api.method` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"GET"` |
| `api.body` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `BodyInit` |
| `api.headers` | VariableDeclaration | HTTP headers, including origin or authentication as needed. | `Record<string, string>` |
| `api.response` | VariableDeclaration | Outgoing HTTP response or inspected fetch result. | `await fetch("/api" + path, { method, headers, body, credentials: "same-origin", })` |
| `api.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `await response.json()` |
| `api.detail` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `typeof data.detail === "string" ? data.detail : t("Revisa los campos y sus límites.")` |
| `module.artifactUrl` | VariableDeclaration | Build a navigable artifact URL without exposing the job token in the query string. | `( job: Job, kind: string, download = false, revision = 0, ) => `/api/jobs/${job.id}/artifacts/${kind}?download=${download}&revision=${revision}`` |
| `module.callback@51` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `module.kind` | Parameter | Allowlisted operation/artifact key, not an arbitrary filename. | `string` |
| `module.download` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `false` |
| `module.revision` | Parameter | Cache-busting counter incremented when artifacts/settings change. | `0` |

## frontend/src/DesignActions.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.DesignActions` | FunctionDeclaration | Group save feedback and explicit continuation; pending changes prevent approval. | `{ dirty, disabled, saved, onSave, onContinue, disabledMessage, }: { dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?:` |
| `DesignActions.dirty` | Parameter | Whether draft settings/text differ from the saved version. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.saved` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.onSave` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.onContinue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.disabledMessage` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ dirty: boolean; disabled: boolean; saved: boolean; onSave: () => void; onContinue: () => void; disabledMessage?: string; }` |
| `DesignActions.dirty` | PropertySignature | Whether draft settings/text differ from the saved version. | `boolean` |
| `DesignActions.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `DesignActions.saved` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `DesignActions.onSave` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `() => void` |
| `DesignActions.onContinue` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `() => void` |
| `DesignActions.disabledMessage` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |

## frontend/src/DesignEntry.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.DesignEntry` | FunctionDeclaration | Offer manual setup or JSON import without automatically approving the background. | `{ method, setMethod, disabled, imported, onImport, }: { method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImpor` |
| `DesignEntry.method` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImport: (file: File) => void; }` |
| `DesignEntry.setMethod` | Parameter | React state setter for method. Schedules a rerender, not a server mutation. | `{ method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImport: (file: File) => void; }` |
| `DesignEntry.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImport: (file: File) => void; }` |
| `DesignEntry.imported` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImport: (file: File) => void; }` |
| `DesignEntry.onImport` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ method: "manual" \| "import"; setMethod: (method: "manual" \| "import") => void; disabled: boolean; imported: boolean; onImport: (file: File) => void; }` |
| `DesignEntry.method` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"manual" \| "import"` |
| `DesignEntry.setMethod` | PropertySignature | React state setter for method. Schedules a rerender, not a server mutation. | `(method: "manual" \| "import") => void` |
| `DesignEntry.method` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"manual" \| "import"` |
| `DesignEntry.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `DesignEntry.imported` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `DesignEntry.onImport` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(file: File) => void` |
| `DesignEntry.file` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `File` |
| `DesignEntry.callback@26` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DesignEntry.callback@37` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DesignEntry.callback@50` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DesignEntry.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DesignEntry.file` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.currentTarget.files?.[0]` |

## frontend/src/i18n.ts

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.Locale` | TypeAliasDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"en" \| "es"` |
| `module.key` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"easypodcast-language"` |
| `module.catalog` | VariableDeclaration | Spanish UI keys mapped to English display strings. | `Record<string, string>` |
| `module.reverse` | VariableDeclaration | English-to-Spanish lookup for stored translated UI errors. | `Object.fromEntries( Object.entries(catalog).map(([es, en]) => [en, es]), )` |
| `module.callback@8` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.es` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.en` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.fragments` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Object.entries(catalog) .filter(([es]) => es.length > 12 \|\| es === "El archivo ") .sort((a, b) => b[0].length - a[0].length)` |
| `module.callback@12` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.es` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.callback@13` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.a` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.b` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.listeners` | VariableDeclaration | Subscribers notified when the locale store changes. | `new Set<() => void>()` |
| `module.readLocale` | FunctionDeclaration | Read the stored supported locale or fall back to English. | `` |
| `module.locale` | VariableDeclaration | Interface language en/es; does not translate episode content. | `Locale` |
| `module.getLocale` | FunctionDeclaration | Expose the current in-memory locale snapshot for React subscriptions. | `` |
| `module.setLocale` | FunctionDeclaration | Persist the locale, update document language/title and notify subscribers. | `value: Locale` |
| `setLocale.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Locale` |
| `setLocale.callback@43` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `setLocale.notify` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.useLocale` | FunctionDeclaration | Subscribe React to the locale store without placing preferences in episode state. | `` |
| `useLocale.callback@48` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `useLocale.notify` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `useLocale.callback@50` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `useLocale.callback@55` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.t` | FunctionDeclaration | Translate only known interface messages; never pass user-authored episode content here. | `value: string` |
| `t.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `t.callback@68` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `t.result` | Parameter | Result of the operation/parser/API named by its assignment. | `` |
| `t.es` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `t.en` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## frontend/src/LanguageSelector.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.LanguageSelector` | FunctionDeclaration | Switch the UI locale while leaving spoken audio language and episode text unchanged. | `` |
| `LanguageSelector.locale` | VariableDeclaration | Interface language en/es; does not translate episode content. | `useLocale()` |
| `LanguageSelector.callback@10` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `LanguageSelector.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## frontend/src/main.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.App` | FunctionDeclaration | Own the current job, token, editable design and four-step workflow; subscribe to UI locale changes. | `` |
| `App.locale` | VariableDeclaration | Interface language en/es; does not translate episode content. | `useLocale()` |
| `App.text` | VariableDeclaration | Subtitle/title text; escape before ASS insertion and never translate user content. | `getText()` |
| `App.callback@24` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.caps` | VariableDeclaration | Backend dependency/limit snapshot used to enable features. | `useState<Capabilities \| null>(null)` |
| `App.setCaps` | VariableDeclaration | React state setter for caps. Schedules a rerender, not a server mutation. | `useState<Capabilities \| null>(null)` |
| `App.job` | VariableDeclaration | Temporary episode with metadata, files, approvals and cancellation resources. | `useState<Job \| null>(null)` |
| `App.setJob` | VariableDeclaration | React state setter for job. Schedules a rerender, not a server mutation. | `useState<Job \| null>(null)` |
| `App.token` | VariableDeclaration | Secret authentication value held in memory and sent in X-Job-Token. | `useState("")` |
| `App.setToken` | VariableDeclaration | React state setter for token. Schedules a rerender, not a server mutation. | `useState("")` |
| `App.design` | VariableDeclaration | Validated episode appearance/encoding settings or unsaved browser draft. | `useState<Design \| null>(null)` |
| `App.setDesign` | VariableDeclaration | React state setter for design. Schedules a rerender, not a server mutation. | `useState<Design \| null>(null)` |
| `App.step` | VariableDeclaration | Zero-based Files/Design/Preview/Export workflow index. | `useState(0)` |
| `App.setStep` | VariableDeclaration | React state setter for step. Schedules a rerender, not a server mutation. | `useState(0)` |
| `App.busy` | VariableDeclaration | Browser request-in-flight flag preventing duplicate actions. | `useState(false)` |
| `App.setBusy` | VariableDeclaration | React state setter for busy. Schedules a rerender, not a server mutation. | `useState(false)` |
| `App.error` | VariableDeclaration | Safe explanatory failure text; must not expose secrets or raw stderr. | `useState("")` |
| `App.setError` | VariableDeclaration | React state setter for error. Schedules a rerender, not a server mutation. | `useState("")` |
| `App.start` | VariableDeclaration | Start time in seconds; in multipart callbacks, byte-slice start index. | `useState(0)` |
| `App.setStart` | VariableDeclaration | React state setter for start. Schedules a rerender, not a server mutation. | `useState(0)` |
| `App.revision` | VariableDeclaration | Cache-busting counter incremented when artifacts/settings change. | `useState(0)` |
| `App.setRevision` | VariableDeclaration | React state setter for revision. Schedules a rerender, not a server mutation. | `useState(0)` |
| `App.dirty` | VariableDeclaration | Whether draft settings/text differ from the saved version. | `useState(false)` |
| `App.setDirty` | VariableDeclaration | React state setter for dirty. Schedules a rerender, not a server mutation. | `useState(false)` |
| `App.designMethod` | VariableDeclaration | Manual setup or JSON-import choice. | `useState<"manual" \| "import">( "manual", )` |
| `App.setDesignMethod` | VariableDeclaration | React state setter for designMethod. Schedules a rerender, not a server mutation. | `useState<"manual" \| "import">( "manual", )` |
| `App.importedDesign` | VariableDeclaration | Whether JSON settings were successfully imported. | `useState(false)` |
| `App.setImportedDesign` | VariableDeclaration | React state setter for importedDesign. Schedules a rerender, not a server mutation. | `useState(false)` |
| `App.savedDesign` | VariableDeclaration | Whether the current design has a successful save confirmation. | `useState(false)` |
| `App.setSavedDesign` | VariableDeclaration | React state setter for savedDesign. Schedules a rerender, not a server mutation. | `useState(false)` |
| `App.unavailable` | VariableDeclaration | Whether polling/action detected a missing/expired/invalid job. | `useState(false)` |
| `App.setUnavailable` | VariableDeclaration | React state setter for unavailable. Schedules a rerender, not a server mutation. | `useState(false)` |
| `App.subtitleMode` | VariableDeclaration | Initial subtitle source: upload or generate. | `useState<"upload" \| "generate">( "upload", )` |
| `App.setSubtitleMode` | VariableDeclaration | React state setter for subtitleMode. Schedules a rerender, not a server mutation. | `useState<"upload" \| "generate">( "upload", )` |
| `App.language` | VariableDeclaration | Spoken audio language sent to Whisper, not interface locale. | `useState("en")` |
| `App.setLanguage` | VariableDeclaration | React state setter for language. Schedules a rerender, not a server mutation. | `useState("en")` |
| `App.transcriptionModel` | VariableDeclaration | Local Whisper Tiny/Base selection. | `useState("tiny")` |
| `App.setTranscriptionModel` | VariableDeclaration | React state setter for transcriptionModel. Schedules a rerender, not a server mutation. | `useState("tiny")` |
| `App.heading` | VariableDeclaration | React ref used to focus the newly selected workflow heading. | `useRef<HTMLHeadingElement>(null)` |
| `App.active` | VariableDeclaration | Whether the job is queued/running/cancelling. | `isActive(job)` |
| `App.callback@51` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@54` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@56` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@59` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.stopped` | VariableDeclaration | Effect cleanup guard preventing stale polling state updates. | `false` |
| `App.timer` | VariableDeclaration | Polling interval handle cleared when the effect is disposed. | `setInterval(() => { api<Job>(`/jobs/${job.id}`, token) .then((next) => { if (stopped) return; setJob((previous) => { if (isActive(previous) && !isActive(next)) setRevision((r) => r` |
| `App.callback@62` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@64` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.next` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@66` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.previous` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@68` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@72` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@81` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.perform` | FunctionDeclaration | Run an async action with busy/error feedback and recognize an unavailable job. | `action: () => Promise<void>` |
| `App.perform.action` | Parameter | POST one authenticated operation and replace the local job snapshot. | `() => Promise<void>` |
| `App.perform.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload` | FunctionDeclaration | Submit selected File objects as multipart data and enter design or subtitle review. | `event: React.FormEvent<HTMLFormElement>` |
| `App.upload.event` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `React.FormEvent<HTMLFormElement>` |
| `App.upload.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `new FormData(event.currentTarget)` |
| `App.upload.key` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload.callback@107` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job & { token: string }>( `/jobs?subtitle_mode=${subtitleMode}&language=${language}&model=${transcriptionModel}`, undefined, "POST", data, )` |
| `App.upload.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `App.change` | FunctionDeclaration | Update one draft Design field and mark it unsaved without contacting the backend. | `key: K, value: Design[K]` |
| `App.change.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `K` |
| `App.change.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design[K]` |
| `App.change.callback@127` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.change.d` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save` | FunctionDeclaration | Persist the complete Design and refresh the job snapshot only after success. | `` |
| `App.save.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job>( `/jobs/${job.id}/config`, token, "PATCH", JSON.stringify(design), )` |
| `App.save.callback@144` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.importDesign` | FunctionDeclaration | Read a bounded design JSON, validate it through the backend and retain the previous design on failure. | `file: File` |
| `App.importDesign.file` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `File` |
| `App.importDesign.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `unknown` |
| `App.importDesign.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job>( `/jobs/${job.id}/config`, token, "PATCH", JSON.stringify(data), )` |
| `App.importDesign.callback@172` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.importDesign.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.action` | FunctionDeclaration | POST one authenticated operation and replace the local job snapshot. | `path: string, body?: unknown` |
| `App.action.path` | Parameter | Controlled filesystem location, never an uploaded filename. | `string` |
| `App.action.body` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `unknown` |
| `App.disabled` | VariableDeclaration | Combined gate for busy, active or unavailable episodes. | `busy \|\| active \|\| unavailable` |
| `App.saveRetainedDesign` | FunctionDeclaration | Download the in-memory design without needing an available backend job. | `` |
| `App.saveRetainedDesign.url` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `URL.createObjectURL( new Blob([JSON.stringify(design, null, 2)], { type: "application/json" }), )` |
| `App.saveRetainedDesign.link` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `document.createElement("a")` |
| `App.saveRetainedDesign.callback@197` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.mode` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job?.background_mode === "openai" ? text.openai : job?.background_mode === "upload" ? text.uploadMode : text.local` |
| `App.callback@238` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.index` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@244` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@270` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@309` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@342` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@361` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@454` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@464` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.file` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@464` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@475` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@485` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@495` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@515` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@526` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@536` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@559` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@578` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@591` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@618` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@633` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@647` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@663` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@677` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@693` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@704` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@718` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@737` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@748` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@767` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@768` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@769` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@785` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@785` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@821` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@827` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@827` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@835` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@836` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@846` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@870` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@870` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1004` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1004` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1028` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.w` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `App.callback@1045` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1046` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1077` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.ok` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.mount` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `document.getElementById("root")` |

## frontend/src/SubtitleReview.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.SubtitleReview` | FunctionDeclaration | Load, edit and explicitly approve SRT while preserving honest word-timing availability. | `{ job, token, onChange, onContinue, }: { job: Job; token: string; onChange: (job: Job) => void; onContinue: () => void; }` |
| `SubtitleReview.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; token: string; onChange: (job: Job) => void; onContinue: () => void; }` |
| `SubtitleReview.token` | Parameter | Secret authentication value held in memory and sent in X-Job-Token. | `{ job: Job; token: string; onChange: (job: Job) => void; onContinue: () => void; }` |
| `SubtitleReview.onChange` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ job: Job; token: string; onChange: (job: Job) => void; onContinue: () => void; }` |
| `SubtitleReview.onContinue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ job: Job; token: string; onChange: (job: Job) => void; onContinue: () => void; }` |
| `SubtitleReview.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `SubtitleReview.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `SubtitleReview.onChange` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job: Job) => void` |
| `SubtitleReview.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `SubtitleReview.onContinue` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `() => void` |
| `SubtitleReview.srt` | VariableDeclaration | SRT under review; editing intentionally discards word alignment. | `useState("")` |
| `SubtitleReview.setSrt` | VariableDeclaration | React state setter for srt. Schedules a rerender, not a server mutation. | `useState("")` |
| `SubtitleReview.original` | VariableDeclaration | Last saved SRT text for dirty-state comparison. | `useState("")` |
| `SubtitleReview.setOriginal` | VariableDeclaration | React state setter for original. Schedules a rerender, not a server mutation. | `useState("")` |
| `SubtitleReview.error` | VariableDeclaration | Safe explanatory failure text; must not expose secrets or raw stderr. | `useState("")` |
| `SubtitleReview.setError` | VariableDeclaration | React state setter for error. Schedules a rerender, not a server mutation. | `useState("")` |
| `SubtitleReview.busy` | VariableDeclaration | Browser request-in-flight flag preventing duplicate actions. | `useState(false)` |
| `SubtitleReview.setBusy` | VariableDeclaration | React state setter for busy. Schedules a rerender, not a server mutation. | `useState(false)` |
| `SubtitleReview.reload` | VariableDeclaration | Counter triggering an explicit subtitle refetch. | `useState(0)` |
| `SubtitleReview.setReload` | VariableDeclaration | React state setter for reload. Schedules a rerender, not a server mutation. | `useState(0)` |
| `SubtitleReview.active` | VariableDeclaration | Whether the job is queued/running/cancelling. | `isActive(job)` |
| `SubtitleReview.callback@24` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.current` | VariableDeclaration | Async cleanup guard against stale/unmounted SRT updates. | `true` |
| `SubtitleReview.srt` | PropertySignature | SRT under review; editing intentionally discards word alignment. | `string` |
| `SubtitleReview.callback@29` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.data` | Parameter | Payload being parsed/transferred; validate before trusting fields. | `` |
| `SubtitleReview.callback@35` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@36` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.run` | FunctionDeclaration | Wrap subtitle operations with busy/error feedback. | `action: () => Promise<void>` |
| `SubtitleReview.run.action` | Parameter | POST one authenticated operation and replace the local job snapshot. | `() => Promise<void>` |
| `SubtitleReview.run.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.dirty` | VariableDeclaration | Whether draft settings/text differ from the saved version. | `srt !== original` |
| `SubtitleReview.callback@76` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@77` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@119` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@125` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@126` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.next` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await api<Job>( `/jobs/${job.id}/subtitles`, token, "PUT", JSON.stringify({ srt }), )` |
| `SubtitleReview.callback@145` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@145` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@154` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@155` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## frontend/src/text.ts

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.getText` | FunctionDeclaration | Compute shared UI labels at render time so language changes remain reactive. | `` |

## frontend/src/ThemeSelector.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.Theme` | TypeAliasDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"classic" \| "studio"` |
| `module.storageKey` | VariableDeclaration | Preference storage key; never contains episode tokens/media. | `"easypodcast-theme"` |
| `module.readTheme` | FunctionDeclaration | Read an explicit browser preference, otherwise use Studio, including blocked storage. | `` |
| `module.ThemeSelector` | FunctionDeclaration | Apply and persist the interface theme without touching episode design. | `` |
| `ThemeSelector.theme` | VariableDeclaration | Interface-only Classic/Studio preference. | `useState<Theme>(readTheme)` |
| `ThemeSelector.setTheme` | VariableDeclaration | React state setter for theme. Schedules a rerender, not a server mutation. | `useState<Theme>(readTheme)` |
| `ThemeSelector.callback@18` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ThemeSelector.callback@30` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ThemeSelector.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## frontend/src/types.ts

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.Design` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Design.title` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Design.description` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Design.image_style` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"illustration" \| "realistic"` |
| `Design.atmosphere` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Design.visualizer` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"waveform" \| "spectrum"` |
| `Design.color` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Design.sensitivity` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.wave_y` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.wave_height` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.font_size` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.subtitle_font` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `\| "sans" \| "serif" \| "mono" \| "nunito" \| "fredoka" \| "quicksand" \| "poppins" \| "baloo2" \| "outfit" \| "balsamiqsans" \| "lexend" \| "atkinsonhyperlegible" \| "comicneue"` |
| `Design.title_font` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design["subtitle_font"]` |
| `Design.title_bold` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Design.title_font_size` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.title_offset_x` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.title_offset_y` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.logo_position` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `\| "top-left" \| "top-right" \| "middle-left" \| "middle-right" \| "bottom-left" \| "bottom-right"` |
| `Design.logo_margin` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.subtitle_color` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Design.outline` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.subtitle_margin` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.subtitle_width` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.max_lines` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.crf` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Design.preset` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"ultrafast" \| "veryfast" \| "fast" \| "medium"` |
| `Design.trim_subtitles` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Design.highlight_words` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Design.highlight_color` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `module.Job` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Job.id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Job.state` | PropertySignature | Lifecycle enum, independent of interface language. | `string` |
| `Job.phase` | PropertySignature | Human-readable description of the current operation. | `string` |
| `Job.progress` | PropertySignature | Processed fraction from 0 to 1, or None/null for indeterminate work. | `number \| null` |
| `Job.error` | PropertySignature | Safe explanatory failure text; must not expose secrets or raw stderr. | `string \| null` |
| `Job.metadata` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ duration: number; audio_tracks: number; codec: string }` |
| `Job.duration` | PropertySignature | Audio or clip length in seconds. | `number` |
| `Job.audio_tracks` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Job.codec` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Job.warnings` | PropertySignature | Nonfatal review messages such as overlap or estimated timing. | `string[]` |
| `Job.config` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design` |
| `Job.background_approved` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Job.preview_approved` | PropertySignature | Whether the current preview was explicitly reviewed. | `boolean` |
| `Job.background_mode` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Job.artifacts` | PropertySignature | Available output kinds; stale renders are discarded after edits. | `string[]` |
| `Job.expires_at` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `Job.subtitle_source` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"upload" \| "generate"` |
| `Job.subtitles_ready` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Job.subtitles_approved` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Job.word_timestamps` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `module.Capabilities` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Capabilities.ffmpeg` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.ffprobe` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.h264` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.aac` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.font` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.filters` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Record<string, boolean>` |
| `Capabilities.render_ready` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.image_provider` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.transcription` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ available: boolean; local: boolean; word_timestamps: boolean; models: string[]; languages: string[]; model_download_allowed: boolean; }` |
| `Capabilities.available` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.local` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.word_timestamps` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.models` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string[]` |
| `Capabilities.languages` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string[]` |
| `Capabilities.model_download_allowed` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Capabilities.limits` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ audio_bytes: number; srt_bytes: number; image_bytes: number; duration_seconds: number; pixels: number; queue: number; concurrent_renders: number; jobs: number; }` |
| `Capabilities.audio_bytes` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.srt_bytes` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.image_bytes` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.duration_seconds` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.pixels` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.queue` | PropertySignature | Bounded FIFO of pending operations consumed by one worker. | `number` |
| `Capabilities.concurrent_renders` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `Capabilities.jobs` | PropertySignature | In-memory registry indexed by random job ID; lost on restart. | `number` |

## frontend/src/TypographyControls.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.fontFamilies` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ sans: "EpisodeSans", serif: "EpisodeSerif", mono: "EpisodeMono", nunito: "EpisodeNunito", fredoka: "EpisodeFredoka", quicksand: "EpisodeQuicksand", poppins: "EpisodePoppins", bal` |
| `module.fontChoices` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[ ["sans", "Sans · DejaVu Sans"], ["serif", "Serif · DejaVu Serif"], ["mono", "Monoespaciada · DejaVu Sans Mono"], ["nunito", "Nunito · redondeada y amable"], ["fredoka", "Fredoka ` |
| `module.logoChoices` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[ ["top-left", "Arriba a la izquierda"], ["top-right", "Arriba a la derecha"], ["middle-left", "Centro a la izquierda"], ["middle-right", "Centro a la derecha"], ["bottom-left", "A` |
| `module.logoStyle` | FunctionDeclaration | Map the six logo placements to percentage-based composition CSS. | `design: Design` |
| `logoStyle.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `Design` |
| `logoStyle.left` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_position.endsWith("left")` |
| `logoStyle.middle` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_position.startsWith("middle")` |
| `module.TypographyControls` | FunctionDeclaration | Edit independent title/subtitle fonts, title offsets and bounded logo placement. | `{ design, disabled, hasLogo, change, }: { design: Design; disabled: boolean; hasLogo: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `TypographyControls.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `{ design: Design; disabled: boolean; hasLogo: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `TypographyControls.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ design: Design; disabled: boolean; hasLogo: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `TypographyControls.hasLogo` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ design: Design; disabled: boolean; hasLogo: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `TypographyControls.change` | Parameter | Update one draft Design field and mark it unsaved without contacting the backend. | `{ design: Design; disabled: boolean; hasLogo: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `TypographyControls.design` | PropertySignature | Validated episode appearance/encoding settings or unsaved browser draft. | `Design` |
| `TypographyControls.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `TypographyControls.hasLogo` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `TypographyControls.change` | PropertySignature | Update one draft Design field and mark it unsaved without contacting the backend. | `<K extends keyof Design>(key: K, value: Design[K]) => void` |
| `TypographyControls.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `K` |
| `TypographyControls.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design[K]` |
| `TypographyControls.callback@90` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@106` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@124` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@135` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@139` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@155` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@166` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@170` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@186` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@196` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@200` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@216` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## transcription/worker.mjs

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.selectWords` | FunctionDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `chunks, offset, coreStart, coreEnd, duration` |
| `selectWords.chunks` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.offset` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.coreStart` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.coreEnd` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.duration` | Parameter | Audio or clip length in seconds. | `` |
| `selectWords.callback@8` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.chunk` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `selectWords.a` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `chunk.timestamp ?? []` |
| `selectWords.b` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `chunk.timestamp ?? []` |
| `selectWords.start` | VariableDeclaration | Start time in seconds; in multipart callbacks, byte-slice start index. | `Math.max(0, a+offset)` |
| `selectWords.end` | VariableDeclaration | Interval end in seconds; in multipart callbacks, byte-slice end index. | `Math.min(duration,b+offset)` |
| `selectWords.middle` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(start+end)/2` |
| `selectWords.text` | VariableDeclaration | Subtitle/title text; escape before ASS insertion and never translate user content. | `String(chunk.text ?? '').replace(/[\x00-\x1f]+/g,' ').trim()` |
| `module.audible` | FunctionDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `samples` |
| `audible.samples` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `audible.sum` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `audible.value` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.main` | FunctionDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `main.input` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.argv.slice(2)` |
| `main.output` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.argv.slice(2)` |
| `main.profile` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.argv.slice(2)` |
| `main.language` | VariableDeclaration | Spoken audio language sent to Whisper, not interface locale. | `process.argv.slice(2)` |
| `main.cache` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.argv.slice(2)` |
| `main.download` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.argv.slice(2)` |
| `main.emit` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `event => process.stdout.write(JSON.stringify(event)+'\n')` |
| `main.callback@29` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `main.event` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `main.pipeline` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await import('@huggingface/transformers')` |
| `main.env` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await import('@huggingface/transformers')` |
| `main.transcriber` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await pipeline('automatic-speech-recognition',`Xenova/whisper-${profile}`,{ device:'cpu',dtype:'q8',session_options:{intraOpNumThreads:2,interOpNumThreads:1}, })` |
| `main.file` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await open(input,'r')` |
| `main.duration` | VariableDeclaration | Audio or clip length in seconds. | `(await file.stat()).size/64000` |
| `main.words` | VariableDeclaration | Validated recognized word intervals used for grouping/highlighting. | `[]` |
| `main.core` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `0` |
| `main.begin` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.max(0,core-5)` |
| `main.finish` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.min(duration,core+25)` |
| `main.buffer` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Buffer.alloc(Math.round((finish-begin)*16000)*4)` |
| `main.bytesRead` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await file.read(buffer,0,buffer.length,Math.round(begin*16000)*4)` |
| `main.samples` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `new Float32Array(bytesRead/4)` |
| `main.i` | VariableDeclaration | Zero-based iteration index local to the current loop. | `0` |
| `main.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await transcriber(samples,{return_timestamps:'word',task:'transcribe', ...(language==='auto'?{}:{language})})` |
| `main.selected` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `selectWords(result.chunks,begin,core,Math.min(duration,core+20),duration)` |
| `main.word` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `main.previous` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `words.at(-1)` |
| `module.callback@69` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

