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
| `library_root` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Path.home() / '.easypodcast' / 'library'` |
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

Source: [backend/app/jobs.py:25](../backend/app/jobs.py).

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
| `project_id` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |
| `archive_error` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |

### `Job.public(self)`

Return the token-free job snapshot exposed by status polling.

Source: [backend/app/jobs.py:55](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `self.cues` |

### `Store()`

Own the in-memory registry, locks, bounded queue, worker and managed cleanup.

Source: [backend/app/jobs.py:82](../backend/app/jobs.py).

### `Store.__init__(self)`

Initialize the instance resources; background threads are started separately.

Source: [backend/app/jobs.py:85](../backend/app/jobs.py).

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

Source: [backend/app/jobs.py:94](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `path.name` |
| `marker` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `self.root / '.easypodcast-root'` |
| `self.file_lock` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FileLock(str(self.root / '.instance.lock'), thread_local=False)` |
| `path` | Controlled filesystem location, never an uploaded filename. | `self.root.iterdir()` |
| `self.worker` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=self.work, daemon=True)` |
| `self.cleaner` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.Thread(target=self.clean_loop, daemon=True)` |

### `Store.close(self)`

Request cancellation, join background threads and release managed resources and the root lock.

Source: [backend/app/jobs.py:113](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `self.jobs.values()` |

### `Store.remove_path(self, path)`

Remove only a direct managed child, without following a symbolic link.

Source: [backend/app/jobs.py:127](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `path`: Controlled filesystem location, never an uploaded filename.

### `Store.new_path(self)`

Create a UUID-named directory and return its ID and path.

Source: [backend/app/jobs.py:136](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `jid` | Random public job ID; a separate secret token is required. | `uuid.uuid4().hex` |
| `path` | Controlled filesystem location, never an uploaded filename. | `self.root / jid` |

### `Store.enqueue(self, job, kind, start=0)`

Queue a copied Design snapshot after checking busy and queue-capacity constraints.

Source: [backend/app/jobs.py:143](../backend/app/jobs.py).

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

### `Store.checkpoint(self, job)`

Keep a durable recovery copy; expose save failures instead of hiding them.

Source: [backend/app/jobs.py:156](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.archive_error` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None` |

### `Store.invalidate(self, job)`

Discard preview/video artifacts and clear approval after a design or input change.

Source: [backend/app/jobs.py:169](../backend/app/jobs.py).

- `self`: The current Python class instance.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `kind` | Allowlisted operation/artifact key, not an arbitrary filename. | `('preview', 'video')` |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |

### `Store.work(self)`

Consume queued operations serially, publish validated artifacts and update retention/state.

Source: [backend/app/jobs.py:176](../backend/app/jobs.py).

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

Source: [backend/app/jobs.py:264](../backend/app/jobs.py).

- `self`: The current Python class instance.

### `Store.cleanup(self)`

Cancel overdue active jobs and remove expired/deleted idle jobs without active readers.

Source: [backend/app/jobs.py:269](../backend/app/jobs.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `now` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time()` |
| `jid` | Random public job ID; a separate secret token is required. | `list(self.jobs.items())` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `list(self.jobs.items())` |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'cancelling'` |

### `make_job(jid, path, meta, cues, warnings)`

Construct a temporary job with a random token and initial validated metadata.

Source: [backend/app/jobs.py:286](../backend/app/jobs.py).

- `jid`: Random public job ID; a separate secret token is required.
- `path`: Controlled filesystem location, never an uploaded filename.
- `meta`: Inspected audio metadata including duration and selected stream.
- `cues`: Ordered subtitle intervals with optional estimated word timing.
- `warnings`: Nonfatal review messages such as overlap or estimated timing.

## backend/app/library.py

Durable local projects and brand templates, separate from disposable render workspaces.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `LOCK` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `threading.RLock()` |
| `FILES` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('audio.bin', 'background.png', 'background-source.png', 'logo.png', 'original.srt', 'generated.srt', 'preview.mp4', 'video.mp4')` |

### `root()`

Prepare an exclusive persistent directory; never reuse an unrelated populated folder.

Source: [backend/app/library.py:33](../backend/app/library.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `directory` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `settings.library_root.expanduser().absolute()` |
| `marker` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `directory / '.easypodcast-library'` |

### `database()`

Open a short-lived SQLite connection; callers serialize file/database changes with LOCK.

Source: [backend/app/library.py:49](../backend/app/library.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `path` | Controlled filesystem location, never an uploaded filename. | `root() / 'library.sqlite3'` |
| `connection` | Short-lived SQLite connection, committed and closed by the context manager. | `sqlite3.connect(path, timeout=30)` |
| `connection.row_factory` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `sqlite3.Row` |

### `owner_key()`

Return a machine-local library capability; it is never placed in localStorage or URLs.

Source: [backend/app/library.py:70](../backend/app/library.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `path` | Controlled filesystem location, never an uploaded filename. | `root() / '.owner-key'` |

### `authorize(request)`

Require the HttpOnly local-library session established by an origin-checked POST.

Source: [backend/app/library.py:82](../backend/app/library.py).

- `request`: HTTP request containing headers and a streamed body.

### `directory(kind, identifier)`

Resolve only UUID child directories inside an allowlisted library collection.

Source: [backend/app/library.py:88](../backend/app/library.py).

- `kind`: Allowlisted operation/artifact key, not an arbitrary filename.
- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `identifier` |
| `parent` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `root() / kind` |
| `target` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `parent / identifier` |

### `copy_file(source, target)`

Publish one copied media file atomically without reading its entire contents into memory.

Source: [backend/app/library.py:107](../backend/app/library.py).

- `source`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `target`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `partial` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `target.with_name(uuid.uuid4().hex + '.partial')` |

### `checkpoint(job)`

Save metadata and changed media; never serialize job tokens, thread events or subprocesses.

Source: [backend/app/library.py:121](../backend/app/library.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `c.words` |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `identifier` | Allowlisted UUID key for a durable project/template, never an arbitrary path. | `job.project_id or uuid.uuid4().hex` |
| `job.project_id` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `identifier` |
| `target` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `directory('projects', identifier)` |
| `existing` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `connection.execute('SELECT snapshot FROM projects WHERE id=?', (identifier,)).fetchone()` |
| `previous` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `json.loads(existing['snapshot']) if existing else {}` |
| `fingerprints` | Size/mtime pairs used to avoid recopying unchanged media after each settings save. | `previous.get('files', {})` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FILES` |
| `source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.path / name` |
| `stamp` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[source.stat().st_size, source.stat().st_mtime_ns]` |
| `snapshot` | Portable project metadata and media fingerprints, excluding secret tokens/process state. | `{'schema_version': 1, 'metadata': job.meta, 'warnings': job.warnings, 'config': job.design.model_dump(), 'cues': [{'start': c.start, 'end': c.end, 'text': c.text, 'words': [w.model_dump() for w in c.w` |
| `now` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time()` |

### `projects()`

List durable project summaries without secrets or local filesystem paths.

Source: [backend/app/library.py:180](../backend/app/library.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `connection.execute('SELECT id,title,created,updated,state,(draft IS NOT NULL) AS has_draft FROM projects ORDER BY updated DESC')` |

### `project(identifier)`

Read a known project record before resolving any media paths.

Source: [backend/app/library.py:191](../backend/app/library.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `connection.execute('SELECT * FROM projects WHERE id=?', (identifier,)).fetchone()` |

### `save_draft(identifier, design, base)`

Persist a validated draft without silently approving it or modifying an active render.

Source: [backend/app/library.py:200](../backend/app/library.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `base`: Last saved Design version used to reject obsolete in-flight autosave requests.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `record` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `project(identifier)` |

### `restore(identifier, store, duplicate=False)`

Create a fresh temporary job/token from durable files; interrupted operations never auto-restart.

Source: [backend/app/library.py:213](../backend/app/library.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `store`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `duplicate`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `c['words']` |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['cues']` |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `project(identifier)` |
| `saved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `json.loads(row['snapshot'])` |
| `source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `directory('projects', identifier)` |
| `jid` | Random public job ID; a separate secret token is required. | `store.new_path()` |
| `target` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `store.new_path()` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['files']` |
| `cues` | Ordered subtitle intervals with optional estimated word timing. | `[Cue(c['start'], c['end'], c['text'], tuple((Word.model_validate(w) for w in c['words'])), c.get('word_offset', 0)) for c in saved['cues']]` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `make_job(jid, target, saved['metadata'], cues, saved['warnings'])` |
| `job.design` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design.model_validate_json(row['draft']) if row['draft'] else Design.model_validate(saved['config'])` |
| `job.project_id` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `None if duplicate else identifier` |
| `job.artifacts` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `set(saved['artifacts'])` |
| `job.background_mode` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['background_mode']` |
| `job.approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['background_approved']` |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['preview_approved']` |
| `job.subtitle_source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['subtitle_source']` |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `saved['subtitles_approved']` |
| `job.transcription_options` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `TranscriptionOptions.model_validate(saved['transcription_options'])` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'Project recovered. Review the design before continuing.'` |
| `job.design.title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job.design.title[:110] + ' (copy)')[:120]` |

### `save_template(job, title)`

Save brand settings plus reusable background/logo, without copying source audio or subtitles.

Source: [backend/app/library.py:271](../backend/app/library.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.
- `title`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `identifier` | Allowlisted UUID key for a durable project/template, never an arbitrary path. | `uuid.uuid4().hex` |
| `target` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `directory('templates', identifier)` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('background.png', 'background-source.png', 'logo.png')` |
| `source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.path / name` |

### `templates()`

List brand presets without returning their media paths.

Source: [backend/app/library.py:288](../backend/app/library.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `connection.execute('SELECT id,title,updated FROM templates ORDER BY updated DESC')` |

### `apply_template(job, identifier, store)`

Reuse a brand template, retaining this episode's title and transcription content.

Source: [backend/app/library.py:297](../backend/app/library.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.
- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `store`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `connection.execute('SELECT * FROM templates WHERE id=?', (identifier,)).fetchone()` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `Design.model_validate_json(row['design'])` |
| `design.title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job.design.title, job.design.description)` |
| `design.description` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job.design.title, job.design.description)` |
| `design.trim_subtitles` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.design.trim_subtitles` |
| `design.crf` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job.design.crf, job.design.preset)` |
| `design.preset` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job.design.crf, job.design.preset)` |
| `source` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `directory('templates', identifier)` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('background.png', 'background-source.png', 'logo.png')` |
| `job.design` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design` |
| `job.background_mode` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'upload'` |
| `job.approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `False` |

### `clear_draft(identifier)`

Remove a recovery draft only after its configuration was explicitly saved.

Source: [backend/app/library.py:325](../backend/app/library.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.

## backend/app/main.py

FastAPI endpoints, local request guards and authenticated artifact responses.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `app` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `FastAPI(title='EasyPodcast', version='0.5.0', lifespan=lifespan)` |
| `frontend` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ROOT / 'frontend' / 'dist'` |

### `lifespan(app)`

Start the store and compute capabilities at startup; close resources during shutdown.

Source: [backend/app/main.py:25](../backend/app/main.py).

- `app`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `app.state.upload_slot` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `asyncio.Semaphore(1)` |
| `app.state.capabilities` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await asyncio.to_thread(capabilities)` |

### `RequestGuard()`

Enforce allowed browser origins and a total request-body byte budget.

Source: [backend/app/main.py:38](../backend/app/main.py).

### `RequestGuard.__init__(self, app)`

Initialize the instance resources; background threads are started separately.

Source: [backend/app/main.py:41](../backend/app/main.py).

- `self`: The current Python class instance.
- `app`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `self.app` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `app` |

### `RequestGuard.__call__(self, scope, receive, send)`

Handle an ASGI request while preserving middleware or response cleanup guarantees.

Source: [backend/app/main.py:45](../backend/app/main.py).

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

Source: [backend/app/main.py:59](../backend/app/main.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `message` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await receive()` |
| `total` | Accumulated incoming body bytes. | `len(message.get('body', b''))` |

### `invalid(request, exc)`

Convert a validation ValueError into a safe HTTP 422 response.

Source: [backend/app/main.py:75](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `exc`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `health()`

Expose service liveness and version without secrets.

Source: [backend/app/main.py:81](../backend/app/main.py).


### `get_capabilities(request: Request)`

Return dependency and limit checks computed at application startup.

Source: [backend/app/main.py:87](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.

### `get_job(jid: str, request: Request)`

Authenticate the job token and reject absent, expired or invalid sessions.

Source: [backend/app/main.py:92](../backend/app/main.py).

- `jid`: Random public job ID; a separate secret token is required.
- `request`: HTTP request containing headers and a streamed body.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `store.jobs.get(jid)` |
| `token` | Secret authentication value held in memory and sent in X-Job-Token. | `request.headers.get('X-Job-Token', '')` |

### `editable(job)`

Reject edits while an operation or artifact download holds the job.

Source: [backend/app/main.py:112](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `create_job(request: Request, subtitle_mode: Literal['upload', 'generate']='upload', language: Literal['auto', 'en', 'es', 'pt', 'fr', 'de', 'it']='en', model: Literal['tiny', 'base']='tiny')`

Serialize uploads and dispatch creation for the selected subtitle source.

Source: [backend/app/main.py:139](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `subtitle_mode`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `language`: Spoken audio language sent to Whisper, not interface locale.
- `model`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `['audio', 'srt', 'image', 'logo']` |

### `create_uploaded_job(request, subtitle_mode, options)`

Receive and validate uploads, create an episode and optionally queue local transcription.

Source: [backend/app/main.py:154](../backend/app/main.py).

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

Source: [backend/app/main.py:231](../backend/app/main.py).

- `response`: Outgoing HTTP response or inspected fetch result.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `deadline` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.active_deadline + settings.ttl_seconds if job.state in ACTIVE else job.expires` |

### `configure(design: Design, job=Depends(get_job))`

Replace validated Design settings and invalidate previous approvals/artifacts.

Source: [backend/app/main.py:248](../backend/app/main.py).

- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.design` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design` |

### `generate(job=Depends(get_job))`

Queue explicit optional provider generation for the current job.

Source: [backend/app/main.py:261](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `approve_background(job=Depends(get_job))`

Mark the current background reviewed without generating or rendering anything.

Source: [backend/app/main.py:270](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `approve_preview(job=Depends(get_job))`

Mark the current preview reviewed after checking that it exists.

Source: [backend/app/main.py:280](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.preview_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `check_render(job)`

Enforce dependencies, subtitle/background approval, trim permission and disk budget.

Source: [backend/app/main.py:291](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `report` | Preflight readiness, blockers and warnings measured from actual selected fonts. | `inspect(job)` |
| `required` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `settings.min_free_bytes + int(job.meta['duration'] * 1000000)` |

### `preview(body: PreviewRequest, job=Depends(get_job))`

Queue up to 20 seconds from the validated starting offset.

Source: [backend/app/main.py:313](../backend/app/main.py).

- `body`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `export(job=Depends(get_job))`

Queue full-episode export only after the current preview has been approved.

Source: [backend/app/main.py:325](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `cancel(job=Depends(get_job))`

Signal cancellation and expose a cancelling phase without blocking the API.

Source: [backend/app/main.py:337](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.state` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('cancelling', 'Cancelando operación')` |
| `job.phase` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `('cancelling', 'Cancelando operación')` |

### `delete(job=Depends(get_job))`

Request cancellation and deferred deletion of this managed episode.

Source: [backend/app/main.py:347](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.deleting` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `artifact(kind: str, download: bool=False, job=Depends(get_job))`

Serve an allowlisted artifact, holding a reader lease for media streaming.

Source: [backend/app/main.py:361](../backend/app/main.py).

- `kind`: Allowlisted operation/artifact key, not an arbitrary filename.
- `download`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `mapping` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'logo': ('logo.png', 'image/png'), 'audio': ('audio.bin', 'application/octet-stream'), 'subtitles': ('generated.srt' if job.subtitle_source == 'generate' else 'original.srt', 'application/x-subrip'),` |
| `name` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `mapping[kind]` |
| `mime` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `mapping[kind]` |
| `job.readers` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1` |

### `artifact.release()`

Release one download reader and retry deferred cleanup.

Source: [backend/app/main.py:395](../backend/app/main.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.readers` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `1` |

### `artifact.LeasedFileResponse(FileResponse)`

Release a download reader lease even when response streaming fails or disconnects.

Source: [backend/app/main.py:401](../backend/app/main.py).

### `artifact.LeasedFileResponse.__call__(self, scope, receive, send)`

Handle an ASGI request while preserving middleware or response cleanup guarantees.

Source: [backend/app/main.py:404](../backend/app/main.py).

- `self`: The current Python class instance.
- `scope`: ASGI context with path, headers and protocol metadata.
- `receive`: ASGI callable reading incoming body events.
- `send`: ASGI callable sending outgoing response events.

### `retry_transcription(job=Depends(get_job))`

Queue transcription again only for episodes created in generate mode.

Source: [backend/app/main.py:420](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `subtitles(job=Depends(get_job))`

Read the reviewable SRT and expose whether word timestamps exist.

Source: [backend/app/main.py:429](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `path` | Controlled filesystem location, never an uploaded filename. | `job.path / ('generated.srt' if job.subtitle_source == 'generate' else 'original.srt')` |

### `edit_subtitles(body: SubtitleEdit, job=Depends(get_job))`

Validate edited SRT, drop stale word timing and invalidate previous renders.

Source: [backend/app/main.py:445](../backend/app/main.py).

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

Source: [backend/app/main.py:468](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `job.subtitles_approved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `True` |

### `font_file(key: str, bold: bool=False)`

Serve an allowlisted bundled font and reject arbitrary path requests.

Source: [backend/app/main.py:480](../backend/app/main.py).

- `key`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `bold`: Whether to select the actual Bold font/style.

### `library_session()`

Establish a same-origin HttpOnly local-library capability without exposing it to JavaScript.

Source: [backend/app/main.py:492](../backend/app/main.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `response` | Outgoing HTTP response or inspected fetch result. | `JSONResponse({'ready': True})` |

### `project_list(request: Request)`

List durable local projects after local-library authorization.

Source: [backend/app/main.py:502](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `item` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `store.jobs.values()` |
| `result` | Result of the operation/parser/API named by its assignment. | `library.projects()` |
| `row` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `result` |
| `live` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `next((item for item in store.jobs.values() if item.project_id == row['id'] and (not item.deleting)), None)` |

### `project_thumbnail(identifier: str, request: Request)`

Serve a bounded project cover image through the library session.

Source: [backend/app/main.py:518](../backend/app/main.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `request`: HTTP request containing headers and a streamed body.

### `open_project(identifier: str, request: Request)`

Recover or duplicate a durable project into a fresh token-protected workspace.

Source: [backend/app/main.py:529](../backend/app/main.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `request`: HTTP request containing headers and a streamed body.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `item` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `store.jobs.values()` |
| `duplicate` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `request.url.path.endswith('duplicate')` |
| `existing` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `next((item for item in store.jobs.values() if item.project_id == identifier and (not item.deleting)), None)` |
| `record` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `library.project(identifier)` |
| `recovered` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design.model_validate_json(record['draft'])` |
| `existing.design` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `recovered` |
| `existing.expires` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `time.time() + settings.ttl_seconds` |
| `job` | Temporary episode with metadata, files, approvals and cancellation resources. | `existing` |
| `candidates` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[item for item in store.jobs.values() if item.state not in ACTIVE and (not item.readers)]` |
| `oldest` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `min(candidates, key=lambda item: item.expires)` |
| `response` | Outgoing HTTP response or inspected fetch result. | `JSONResponse({**job.public(), 'token': job.token})` |

### `project_draft(identifier: str, body: DraftRequest, request: Request)`

Autosave validated appearance settings without granting render approval.

Source: [backend/app/main.py:581](../backend/app/main.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `body`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `request`: HTTP request containing headers and a streamed body.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `saved` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `library.save_draft(identifier, body.design, body.base)` |

### `template_list(request: Request)`

List reusable brand settings and media stored locally.

Source: [backend/app/main.py:589](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.

### `create_template(request: Request, body: TemplateRequest | None=None, job=Depends(get_job))`

Save the current brand appearance plus background/logo, without audio or captions.

Source: [backend/app/main.py:596](../backend/app/main.py).

- `request`: HTTP request containing headers and a streamed body.
- `body`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `apply_brand(identifier: str, request: Request, job=Depends(get_job))`

Apply a saved brand while retaining this episode's title and spoken content.

Source: [backend/app/main.py:605](../backend/app/main.py).

- `identifier`: Allowlisted UUID key for a durable project/template, never an arbitrary path.
- `request`: HTTP request containing headers and a streamed body.
- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

### `preflight(job=Depends(get_job))`

Check layout/text with real font measurement without starting a render.

Source: [backend/app/main.py:615](../backend/app/main.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

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

### `normalize_image(source: Path, target: Path, logo=False, preserve=False)`

Decode and size-bound an uploaded image before producing a normalized PNG.

Source: [backend/app/media.py:139](../backend/app/media.py).

- `source`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `target`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `logo`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `preserve`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `image` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageOps.exif_transpose(im).convert('RGBA' if logo else 'RGB')` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |

### `local_background(target: Path)`

Draw the deterministic local demonstration background without an external service.

Source: [backend/app/media.py:161](../backend/app/media.py).

- `target`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `image` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Image.new('RGB', (1920, 1080), '#101522')` |
| `draw` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageDraw.Draw(image)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `range(1080)` |

### `terminate(process)`

Stop the subprocess tree/group and wait for it to exit on Windows or POSIX.

Source: [backend/app/media.py:173](../backend/app/media.py).

- `process`: Supervised child process; stop it before releasing the worker.

### `render(job, design, start, duration, output, update)`

Build ASS/filtergraph inputs, supervise FFmpeg and validate the finished MP4 before publication.

Source: [backend/app/media.py:190](../backend/app/media.py).

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
| `frame_width` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.frame_size` |
| `frame_height` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.frame_size` |
| `wave_width` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `round(frame_width * 5 / 6) // 2 * 2` |
| `size` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'{wave_width}x{round(frame_height * design.wave_height) // 2 * 2}'` |
| `color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'0x' + design.color[1:]` |
| `visual` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'showwaves=s={size}:mode=line:rate=30:colors={color}' if design.visualizer == 'waveform' else f'showfreqs=s={size}:mode=bar:ascale=sqrt:fscale=log:colors={color}:rate=30'` |
| `graph` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f"[0:v]scale={frame_width}:{frame_height}:force_original_aspect_ratio=decrease,pad={frame_width}:{frame_height}:(ow-iw)/2:(oh-ih)/2:color=0x101522,setsar=1[bg];[1:{job.meta['audio_stream']}]asplit=2[a` |
| `inputs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[settings.ffmpeg, '-hide_banner', '-nostdin', '-y', '-loop', '1', '-framerate', '30', '-i', 'background-source.png' if (job.path / 'background-source.png').exists() else 'background.png', '-ss', str(s` |
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

Source: [backend/app/media.py:289](../backend/app/media.py).


| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `process.stdout` |

### `render.read_errors()`

Drain bounded FFmpeg error output so a full stderr pipe cannot deadlock rendering.

Source: [backend/app/media.py:298](../backend/app/media.py).


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
| `output_format` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'landscape'` |
| `logo_x` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(None, ge=0, le=1)` |
| `logo_y` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(None, ge=0, le=1)` |
| `logo_scale` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(1, ge=0.25, le=2.5)` |
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

### `Design.frame_size(self)`

Return output dimensions; all layout units are pixels in this frame.

Source: [backend/app/models.py:92](../backend/app/models.py).

- `self`: The current Python class instance.

### `Design.safe_layout(self)`

Reject subtitle and visualizer overlap using canvas-coordinate layout estimates.

Source: [backend/app/models.py:99](../backend/app/models.py).

- `self`: The current Python class instance.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `height` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `self.frame_size[1]` |
| `subtitle_top` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `height - self.subtitle_margin - self.font_size * self.max_lines * 1.25 - 20` |

### `PreviewRequest(BaseModel)`

Validate the nonnegative preview start time in seconds.

Source: [backend/app/models.py:108](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid', allow_inf_nan=False)` |
| `start` | Start time in seconds; in multipart callbacks, byte-slice start index. | `Field(0, ge=0)` |

### `TranscriptionOptions(BaseModel)`

Allowlist the local Whisper model and spoken audio language.

Source: [backend/app/models.py:116](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `language` | Spoken audio language sent to Whisper, not interface locale. | `'en'` |
| `model` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `'tiny'` |

### `SubtitleEdit(BaseModel)`

Bound the size of an edited SRT payload.

Source: [backend/app/models.py:126](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `srt` | SRT under review; editing intentionally discards word alignment. | `Field(min_length=1, max_length=5 * 1024 ** 2)` |

### `DraftRequest(BaseModel)`

Version a recovery draft against the last saved design to reject stale in-flight autosaves.

Source: [backend/app/models.py:134](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `annotation / loop binding` |
| `base` | Last saved Design version used to reject obsolete in-flight autosave requests. | `annotation / loop binding` |

### `TemplateRequest(BaseModel)`

Optional human-readable brand name; never used as a directory or filename.

Source: [backend/app/models.py:142](../backend/app/models.py).

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `model_config` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ConfigDict(extra='forbid')` |
| `title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Field(min_length=1, max_length=120)` |

## backend/app/preflight.py

Pre-render layout review using the actual font measurement and ASS generation rules.

### `overlaps(a, b)`

Return whether two pixel rectangles have a positive-area intersection.

Source: [backend/app/preflight.py:9](../backend/app/preflight.py).

- `a`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `b`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `inspect(job)`

Report blockers and warnings; never charge providers or start an encoder.

Source: [backend/app/preflight.py:14](../backend/app/preflight.py).

- `job`: Temporary episode with metadata, files, approvals and cancellation resources.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job.cues` |
| `line` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `title_lines` |
| `v` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `image.size` |
| `design` | Validated episode appearance/encoding settings or unsaved browser draft. | `job.design` |
| `width` | Available width in video pixels for text wrapping. | `design.frame_size` |
| `height` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.frame_size` |
| `blockers` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `([], list(job.warnings))` |
| `warnings` | Nonfatal review messages such as overlap or estimated timing. | `([], list(job.warnings))` |
| `exc` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `caught exception` |
| `x` | Horizontal title coordinate in video pixels, when used in make_ass. | `(width / 2 + design.title_offset_x, 100 + design.title_offset_y)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `(width / 2 + design.title_offset_x, 100 + design.title_offset_y)` |
| `title_width` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `max(80, min(1600, 2 * (min(x, width - x) - 120)))` |
| `title_lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `wrap_text(design.title, design.title_font, design.title_font_size, title_width, design.title_bold)` |
| `font` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ImageFont.truetype(str(font_path(design.title_font, design.title_bold)), design.title_font_size)` |
| `title` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(x - title_width / 2, y, x + title_width / 2, y + len(title_lines) * design.title_font_size * 1.3)` |
| `subtitle_top` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `height - design.subtitle_margin - design.font_size * design.max_lines * 1.25 - 20` |
| `lw` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(v * design.logo_scale for v in image.size)` |
| `lh` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(v * design.logo_scale for v in image.size)` |
| `lx` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `width - lw - design.logo_margin if design.logo_position.endswith('right') else design.logo_margin` |
| `ly` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(height - lh) / 2 if design.logo_position.startswith('middle') else height - lh - design.logo_margin if design.logo_position.startswith('bottom') else design.logo_margin` |
| `logo` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(lx, ly, lx + lw, ly + lh)` |

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
| `output` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `wrap_text(text, design.subtitle_font, design.font_size, design.frame_size[0] * design.subtitle_width - 40)` |

### `ass_time(seconds: float)`

Format seconds as nonnegative ASS centisecond timestamps.

Source: [backend/app/subtitles.py:138](../backend/app/subtitles.py).

- `seconds`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `cs` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `max(0, round(seconds * 100))` |

### `render_srt(cues)`

Serialize cues using numbered UTF-8 SRT blocks and millisecond timestamps.

Source: [backend/app/subtitles.py:144](../backend/app/subtitles.py).

- `cues`: Ordered subtitle intervals with optional estimated word timing.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `i` | Zero-based iteration index local to the current loop. | `enumerate(cues, 1)` |
| `c` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `enumerate(cues, 1)` |

### `render_srt.stamp(seconds)`

Format seconds as a subtitle timestamp for a generated fixture or SRT.

Source: [backend/app/subtitles.py:147](../backend/app/subtitles.py).

- `seconds`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `ms` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `round(seconds * 1000)` |

### `ass_color(value)`

Convert a validated RGB hex color into ASS BGR notation.

Source: [backend/app/subtitles.py:158](../backend/app/subtitles.py).

- `value`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `value` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `value.lstrip('#')` |

### `highlighted_caption(caption, words, active, design, offset=0)`

Color only the active word while preserving escaped text and clipped offsets.

Source: [backend/app/subtitles.py:164](../backend/app/subtitles.py).

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

Source: [backend/app/subtitles.py:183](../backend/app/subtitles.py).

- `cues`: Ordered subtitle intervals with optional estimated word timing.
- `design`: Validated episode appearance/encoding settings or unsaved browser draft.
- `duration`: Audio or clip length in seconds.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `w` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cue.words` |
| `t` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(w.start, w.end)` |
| `i` | Zero-based iteration index local to the current loop. | `enumerate(cue.words)` |
| `color` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.subtitle_color.lstrip('#')` |
| `frame_width` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.frame_size` |
| `frame_height` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.frame_size` |
| `margin` | Canvas inset measured in video pixels. | `round(frame_width * (1 - design.subtitle_width) / 2)` |
| `header` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `f'[Script Info]\nScriptType: v4.00+\nPlayResX: {frame_width}\nPlayResY: {frame_height}\nWrapStyle: 0\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, Bac` |
| `events` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[]` |
| `x` | Horizontal title coordinate in video pixels, when used in make_ass. | `(frame_width // 2 + design.title_offset_x, 100 + design.title_offset_y)` |
| `y` | Vertical title coordinate in video pixels, when used in make_ass. | `(frame_width // 2 + design.title_offset_x, 100 + design.title_offset_y)` |
| `width` | Available width in video pixels for text wrapping. | `min(1600, 2 * (min(x, frame_width - x) - 120))` |
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
| `ROLES` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{'identifier': 'Allowlisted UUID key for a durable project/template, never an arbitrary path.', 'connection': 'Short-lived SQLite connection, committed and closed by the context manager.', 'snapshot':` |

### `meaning(name)`

Explain a domain variable or a React setter; use source expressions for other locals.

Source: [scripts/build_code_reference.py:106](../scripts/build_code_reference.py).

- `name`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `cell(value)`

Escape source excerpts for a Markdown table.

Source: [scripts/build_code_reference.py:121](../scripts/build_code_reference.py).

- `value`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.

### `python_module(path)`

Inventory Python declarations, parameters and assignments by their lexical scope.

Source: [scripts/build_code_reference.py:126](../scripts/build_code_reference.py).

- `path`: Controlled filesystem location, never an uploaded filename.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `tree` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `ast.parse(path.read_text(encoding='utf-8'))` |
| `relative` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `path.relative_to(ROOT).as_posix()` |
| `lines` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `[f'## {relative}', '', ast.get_docstring(tree) or 'Repository utility module.', '']` |

### `python_module.walk(node, scope='module')`

Render one lexical scope and recursively document nested declarations.

Source: [scripts/build_code_reference.py:132](../scripts/build_code_reference.py).

- `node`: Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting.
- `scope`: ASGI context with path, headers and protocol metadata.

| Variable / attribute | Explanation | Initializer / assignment excerpt |
| --- | --- | --- |
| `b` | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `node.bases` |
| `scope` | ASGI context with path, headers and protocol metadata. | `node.name if scope == 'module' else scope + '.' + node.name` |
| `signature` | Serialized content version; identical polling snapshots do not trigger repeated validation. | `ast.unparse(node.args) if hasattr(node, 'args') else ', '.join((ast.unparse(b) for b in node.bases))` |
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

Source: [scripts/build_code_reference.py:158](../scripts/build_code_reference.py).

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

Source: [scripts/build_code_reference.py:205](../scripts/build_code_reference.py).


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

## frontend/src/CanvasEditor.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.frameSize` | FunctionDeclaration | Resolve landscape, portrait or square frame dimensions with backward-compatible defaults. | `design?: Design \| null` |
| `frameSize.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `Design \| null` |
| `module.canvasDelta` | FunctionDeclaration | Scale pointer deltas from displayed CSS pixels to actual output-frame pixels. | `dx: number, dy: number, rect: { width: number; height: number }, frame: [number, number]` |
| `canvasDelta.dx` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `canvasDelta.dy` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `canvasDelta.rect` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ width: number; height: number }` |
| `canvasDelta.width` | PropertySignature | Available width in video pixels for text wrapping. | `number` |
| `canvasDelta.height` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `canvasDelta.frame` | Parameter | Selected output width/height in pixels, independent of displayed canvas size. | `[number, number]` |
| `module.logoBox` | FunctionDeclaration | Calculate actual logo bounds and clamp free coordinates consistently with FFmpeg. | `design: Design, frame: [number, number], natural: { width: number; height: number }` |
| `logoBox.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `Design` |
| `logoBox.frame` | Parameter | Selected output width/height in pixels, independent of displayed canvas size. | `[number, number]` |
| `logoBox.natural` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ width: number; height: number }` |
| `logoBox.width` | PropertySignature | Available width in video pixels for text wrapping. | `number` |
| `logoBox.height` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `logoBox.width` | VariableDeclaration | Available width in video pixels for text wrapping. | `frame` |
| `logoBox.height` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `frame` |
| `logoBox.position` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_position ?? "top-right"` |
| `logoBox.margin` | VariableDeclaration | Canvas inset measured in video pixels. | `design.logo_margin ?? 40` |
| `logoBox.w` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `natural.width * (design.logo_scale ?? 1)` |
| `logoBox.h` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `natural.height * (design.logo_scale ?? 1)` |
| `logoBox.left` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_x != null ? Math.min(width - w, Math.max(0, width * design.logo_x)) : position.endsWith("right") ? width - w - margin : margin` |
| `logoBox.top` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_y != null ? Math.min(height - h, Math.max(0, height * design.logo_y)) : position.startsWith("middle") ? (height - h) / 2 : position.startsWith("bottom") ? height - h - ` |
| `module.CanvasEditor` | FunctionDeclaration | Map pointer/keyboard edits into output pixels; move/resize title and logo without auto-approval. | `{ job, design, revision, disabled, change, }: { job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `{ job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.revision` | Parameter | Cache-busting counter incremented when artifacts/settings change. | `{ job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.change` | Parameter | Update one draft Design field and mark it unsaved without contacting the backend. | `{ job: Job; design: Design; revision: number; disabled: boolean; change: <K extends keyof Design>(key: K, value: Design[K]) => void; }` |
| `CanvasEditor.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `CanvasEditor.design` | PropertySignature | Validated episode appearance/encoding settings or unsaved browser draft. | `Design` |
| `CanvasEditor.revision` | PropertySignature | Cache-busting counter incremented when artifacts/settings change. | `number` |
| `CanvasEditor.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `CanvasEditor.change` | PropertySignature | Update one draft Design field and mark it unsaved without contacting the backend. | `<K extends keyof Design>(key: K, value: Design[K]) => void` |
| `CanvasEditor.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `K` |
| `CanvasEditor.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design[K]` |
| `CanvasEditor.dragging` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(false)` |
| `CanvasEditor.setDragging` | VariableDeclaration | React state setter for dragging. Schedules a rerender, not a server mutation. | `useState(false)` |
| `CanvasEditor.naturalLogo` | VariableDeclaration | Actual normalized logo dimensions used to match browser and FFmpeg scaling. | `useState({ width: 300, height: 160 })` |
| `CanvasEditor.setNaturalLogo` | VariableDeclaration | React state setter for naturalLogo. Schedules a rerender, not a server mutation. | `useState({ width: 300, height: 160 })` |
| `CanvasEditor.drag` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useRef<{ kind: string; x: number; y: number; offsetX: number; offsetY: number; size: number; left: number; top: number; rect: DOMRect; } \| null>(null)` |
| `CanvasEditor.kind` | PropertySignature | Allowlisted operation/artifact key, not an arbitrary filename. | `string` |
| `CanvasEditor.x` | PropertySignature | Horizontal title coordinate in video pixels, when used in make_ass. | `number` |
| `CanvasEditor.y` | PropertySignature | Vertical title coordinate in video pixels, when used in make_ass. | `number` |
| `CanvasEditor.offsetX` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `CanvasEditor.offsetY` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `CanvasEditor.size` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `CanvasEditor.left` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `CanvasEditor.top` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `CanvasEditor.rect` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `DOMRect` |
| `CanvasEditor.frame` | VariableDeclaration | Selected output width/height in pixels, independent of displayed canvas size. | `frameSize(design)` |
| `CanvasEditor.width` | VariableDeclaration | Available width in video pixels for text wrapping. | `frame` |
| `CanvasEditor.height` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `frame` |
| `CanvasEditor.box` | VariableDeclaration | Logo's top-left and dimensions in output pixels, including free-position clamping. | `logoBox(design, frame, naturalLogo)` |
| `CanvasEditor.limit` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.min(600, width / 2 - 160)` |
| `CanvasEditor.begin` | FunctionDeclaration | Capture a pointer and the original output coordinates before starting a drag/resize. | `e: React.PointerEvent<HTMLElement>, kind: string` |
| `CanvasEditor.begin.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `React.PointerEvent<HTMLElement>` |
| `CanvasEditor.begin.kind` | Parameter | Allowlisted operation/artifact key, not an arbitrary filename. | `string` |
| `CanvasEditor.begin.canvas` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.currentTarget.closest(".canvas")!.getBoundingClientRect()` |
| `CanvasEditor.begin.item` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.currentTarget .closest(".canvas-title,.canvas-logo") ?.getBoundingClientRect() ?? e.currentTarget.getBoundingClientRect()` |
| `CanvasEditor.move` | FunctionDeclaration | Apply the current pointer delta within validated title/logo bounds. | `e: React.PointerEvent<HTMLElement>` |
| `CanvasEditor.move.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `React.PointerEvent<HTMLElement>` |
| `CanvasEditor.move.state` | VariableDeclaration | Lifecycle enum, independent of interface language. | `drag.current` |
| `CanvasEditor.move.dx` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `canvasDelta( e.clientX - state.x, e.clientY - state.y, state.rect, frame, )` |
| `CanvasEditor.move.dy` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `canvasDelta( e.clientX - state.x, e.clientY - state.y, state.rect, frame, )` |
| `CanvasEditor.end` | FunctionDeclaration | Release transient drag state and hide alignment guides. | `` |
| `CanvasEditor.keyboard` | FunctionDeclaration | Move title/logo with arrow keys, using Shift for a larger output-pixel step. | `e: React.KeyboardEvent<HTMLElement>, kind: "title" \| "logo"` |
| `CanvasEditor.keyboard.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `React.KeyboardEvent<HTMLElement>` |
| `CanvasEditor.keyboard.kind` | Parameter | Allowlisted operation/artifact key, not an arbitrary filename. | `"title" \| "logo"` |
| `CanvasEditor.keyboard.amount` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.shiftKey ? 50 : 10` |
| `CanvasEditor.keyboard.dx` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.key === "ArrowLeft" ? -amount : e.key === "ArrowRight" ? amount : 0` |
| `CanvasEditor.keyboard.dy` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.key === "ArrowUp" ? -amount : e.key === "ArrowDown" ? amount : 0` |
| `CanvasEditor.keyboard.rect` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.currentTarget.getBoundingClientRect()` |
| `CanvasEditor.keyboard.canvas` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `e.currentTarget .closest(".canvas")! .getBoundingClientRect()` |
| `CanvasEditor.handlers` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ onPointerMove: move, onPointerUp: end, onPointerCancel: end, }` |
| `CanvasEditor.callback@212` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@213` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@232` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@247` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@248` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@250` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.callback@279` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `CanvasEditor.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

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
| `App.callback@28` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.libraryRevision` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(0)` |
| `App.setLibraryRevision` | VariableDeclaration | React state setter for libraryRevision. Schedules a rerender, not a server mutation. | `useState(0)` |
| `App.editingSubtitles` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(false)` |
| `App.setEditingSubtitles` | VariableDeclaration | React state setter for editingSubtitles. Schedules a rerender, not a server mutation. | `useState(false)` |
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
| `App.callback@57` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@60` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@62` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@65` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.stopped` | VariableDeclaration | Effect cleanup guard preventing stale polling state updates. | `false` |
| `App.timer` | VariableDeclaration | Polling interval handle cleared when the effect is disposed. | `setInterval(() => { api<Job>(`/jobs/${job.id}`, token) .then((next) => { if (stopped) return; setJob((previous) => { if (isActive(previous) && !isActive(next)) setRevision((r) => r` |
| `App.callback@68` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@70` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.next` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@72` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.previous` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@74` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@78` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@87` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.perform` | FunctionDeclaration | Run an async action with busy/error feedback and recognize an unavailable job. | `action: () => Promise<void>` |
| `App.perform.action` | Parameter | POST one authenticated operation and replace the local job snapshot. | `() => Promise<void>` |
| `App.perform.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload` | FunctionDeclaration | Submit selected File objects as multipart data and enter design or subtitle review. | `event: React.FormEvent<HTMLFormElement>` |
| `App.upload.event` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `React.FormEvent<HTMLFormElement>` |
| `App.upload.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `new FormData(event.currentTarget)` |
| `App.upload.key` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload.callback@113` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job & { token: string }>( `/jobs?subtitle_mode=${subtitleMode}&language=${language}&model=${transcriptionModel}`, undefined, "POST", data, )` |
| `App.upload.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `App.upload.callback@121` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.upload.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.change` | FunctionDeclaration | Update one draft Design field and mark it unsaved without contacting the backend. | `key: K, value: Design[K]` |
| `App.change.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `K` |
| `App.change.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Design[K]` |
| `App.change.callback@135` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.change.d` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save` | FunctionDeclaration | Persist the complete Design and refresh the job snapshot only after success. | `` |
| `App.save.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job>( `/jobs/${job.id}/config`, token, "PATCH", JSON.stringify(design), )` |
| `App.save.callback@152` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save.callback@153` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.save.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.importDesign` | FunctionDeclaration | Read a bounded design JSON, validate it through the backend and retain the previous design on failure. | `file: File` |
| `App.importDesign.file` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `File` |
| `App.importDesign.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `unknown` |
| `App.importDesign.result` | VariableDeclaration | Result of the operation/parser/API named by its assignment. | `await api<Job>( `/jobs/${job.id}/config`, token, "PATCH", JSON.stringify(data), )` |
| `App.importDesign.callback@181` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.importDesign.r` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.action` | FunctionDeclaration | POST one authenticated operation and replace the local job snapshot. | `path: string, body?: unknown` |
| `App.action.path` | Parameter | Controlled filesystem location, never an uploaded filename. | `string` |
| `App.action.body` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `unknown` |
| `App.disabled` | VariableDeclaration | Combined gate for busy, active or unavailable episodes. | `busy \|\| active \|\| unavailable` |
| `App.saveRetainedDesign` | FunctionDeclaration | Download the in-memory design without needing an available backend job. | `` |
| `App.saveRetainedDesign.url` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `URL.createObjectURL( new Blob([JSON.stringify(design, null, 2)], { type: "application/json" }), )` |
| `App.saveRetainedDesign.link` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `document.createElement("a")` |
| `App.saveRetainedDesign.callback@206` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.mode` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `job?.background_mode === "openai" ? text.openai : job?.background_mode === "upload" ? text.uploadMode : text.local` |
| `App.callback@247` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.index` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@253` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@263` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@274` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.result` | Parameter | Result of the operation/parser/API named by its assignment. | `` |
| `App.callback@285` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@311` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@350` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@383` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@402` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@495` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@505` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.file` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@505` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@512` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@534` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.result` | Parameter | Result of the operation/parser/API named by its assignment. | `` |
| `App.callback@538` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@543` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@543` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.v` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@552` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@565` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@575` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@585` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@605` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@616` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@626` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@649` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@668` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@681` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@708` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@723` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@737` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@753` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@767` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@783` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@794` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@808` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@827` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@838` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@857` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@858` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@859` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@875` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@875` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@912` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@918` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@918` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@926` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@927` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@937` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@963` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@963` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1069` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1069` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1093` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.w` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `App.callback@1112` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1113` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1119` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.callback@1145` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `App.ok` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.mount` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `document.getElementById("root")` |

## frontend/src/Preflight.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.Report` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Report.ready` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `Report.blockers` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string[]` |
| `Report.warnings` | PropertySignature | Nonfatal review messages such as overlap or estimated timing. | `string[]` |
| `Report.width` | PropertySignature | Available width in video pixels for text wrapping. | `number` |
| `Report.height` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `module.Preflight` | FunctionDeclaration | Display server-measured text/layout blockers and review warnings before preview/export. | `{ job, token, dirty, }: { job: Job; token: string; dirty: boolean; }` |
| `Preflight.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; token: string; dirty: boolean; }` |
| `Preflight.token` | Parameter | Secret authentication value held in memory and sent in X-Job-Token. | `{ job: Job; token: string; dirty: boolean; }` |
| `Preflight.dirty` | Parameter | Whether draft settings/text differ from the saved version. | `{ job: Job; token: string; dirty: boolean; }` |
| `Preflight.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `Preflight.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `Preflight.dirty` | PropertySignature | Whether draft settings/text differ from the saved version. | `boolean` |
| `Preflight.signature` | VariableDeclaration | Serialized content version; identical polling snapshots do not trigger repeated validation. | `JSON.stringify([ job.id, job.config, job.subtitles_approved, job.warnings, job.artifacts, job.state, ])` |
| `Preflight.report` | VariableDeclaration | Preflight readiness, blockers and warnings measured from actual selected fonts. | `useState<Report \| null>(null)` |
| `Preflight.setReport` | VariableDeclaration | React state setter for report. Schedules a rerender, not a server mutation. | `useState<Report \| null>(null)` |
| `Preflight.error` | VariableDeclaration | Safe explanatory failure text; must not expose secrets or raw stderr. | `useState("")` |
| `Preflight.setError` | VariableDeclaration | React state setter for error. Schedules a rerender, not a server mutation. | `useState("")` |
| `Preflight.callback@32` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.current` | VariableDeclaration | Async cleanup guard against stale/unmounted SRT updates. | `true` |
| `Preflight.callback@37` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.callback@40` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.callback@43` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.callback@62` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.item` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `Preflight.callback@67` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.item` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `Preflight.i` | Parameter | Zero-based iteration index local to the current loop. | `` |

## frontend/src/ProjectLibrary.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.ProjectSummary` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectSummary.id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `ProjectSummary.title` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `ProjectSummary.created` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `ProjectSummary.updated` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `ProjectSummary.state` | PropertySignature | Lifecycle enum, independent of interface language. | `string` |
| `ProjectSummary.has_draft` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `module.resumeStep` | FunctionDeclaration | Reopen at the latest subtitle/design/preview/export stage with valid artifacts and approvals. | `job: Job` |
| `resumeStep.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `module.ProjectLibrary` | FunctionDeclaration | List durable local projects and reopen or duplicate them after flushing the current design draft. | `{ onOpen, disabled, revision = 0, beforeOpen, }: { onOpen: (job: Job & { token: string }) => void; disabled: boolean; revision?: number; beforeOpen?: () => Promise<void>; }` |
| `ProjectLibrary.onOpen` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ onOpen: (job: Job & { token: string }) => void; disabled: boolean; revision?: number; beforeOpen?: () => Promise<void>; }` |
| `ProjectLibrary.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ onOpen: (job: Job & { token: string }) => void; disabled: boolean; revision?: number; beforeOpen?: () => Promise<void>; }` |
| `ProjectLibrary.revision` | Parameter | Cache-busting counter incremented when artifacts/settings change. | `{ onOpen: (job: Job & { token: string }) => void; disabled: boolean; revision?: number; beforeOpen?: () => Promise<void>; }` |
| `ProjectLibrary.beforeOpen` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ onOpen: (job: Job & { token: string }) => void; disabled: boolean; revision?: number; beforeOpen?: () => Promise<void>; }` |
| `ProjectLibrary.onOpen` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job: Job & { token: string }) => void` |
| `ProjectLibrary.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job & { token: string }` |
| `ProjectLibrary.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `ProjectLibrary.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `ProjectLibrary.revision` | PropertySignature | Cache-busting counter incremented when artifacts/settings change. | `number` |
| `ProjectLibrary.beforeOpen` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `() => Promise<void>` |
| `ProjectLibrary.details` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useRef<HTMLDetailsElement>(null)` |
| `ProjectLibrary.items` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState<ProjectSummary[]>([])` |
| `ProjectLibrary.setItems` | VariableDeclaration | React state setter for items. Schedules a rerender, not a server mutation. | `useState<ProjectSummary[]>([])` |
| `ProjectLibrary.error` | VariableDeclaration | Safe explanatory failure text; must not expose secrets or raw stderr. | `useState("")` |
| `ProjectLibrary.setError` | VariableDeclaration | React state setter for error. Schedules a rerender, not a server mutation. | `useState("")` |
| `ProjectLibrary.working` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(false)` |
| `ProjectLibrary.setWorking` | VariableDeclaration | React state setter for working. Schedules a rerender, not a server mutation. | `useState(false)` |
| `ProjectLibrary.reload` | VariableDeclaration | Counter triggering an explicit subtitle refetch. | `useState(0)` |
| `ProjectLibrary.setReload` | VariableDeclaration | React state setter for reload. Schedules a rerender, not a server mutation. | `useState(0)` |
| `ProjectLibrary.callback@37` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.current` | VariableDeclaration | Async cleanup guard against stale/unmounted SRT updates. | `true` |
| `ProjectLibrary.ready` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `ProjectLibrary.callback@40` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@41` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.data` | Parameter | Payload being parsed/transferred; validate before trusting fields. | `` |
| `ProjectLibrary.callback@44` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@47` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.open` | FunctionDeclaration | Flush the current draft and request an authenticated saved-project reopen or duplication. | `id: string, duplicate = false` |
| `ProjectLibrary.open.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `ProjectLibrary.open.duplicate` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `false` |
| `ProjectLibrary.open.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `ProjectLibrary.open.callback@65` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.open.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.open.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@84` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@84` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@91` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.item` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@109` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `ProjectLibrary.callback@115` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.DraftAutosave` | FunctionDeclaration | Debounce appearance recovery drafts and reject stale base versions without approving render settings. | `{ job, design, dirty, }: { job: Job; design: Design \| null; dirty: boolean; }` |
| `DraftAutosave.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; design: Design \| null; dirty: boolean; }` |
| `DraftAutosave.design` | Parameter | Validated episode appearance/encoding settings or unsaved browser draft. | `{ job: Job; design: Design \| null; dirty: boolean; }` |
| `DraftAutosave.dirty` | Parameter | Whether draft settings/text differ from the saved version. | `{ job: Job; design: Design \| null; dirty: boolean; }` |
| `DraftAutosave.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `DraftAutosave.design` | PropertySignature | Validated episode appearance/encoding settings or unsaved browser draft. | `Design \| null` |
| `DraftAutosave.dirty` | PropertySignature | Whether draft settings/text differ from the saved version. | `boolean` |
| `DraftAutosave.status` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState("")` |
| `DraftAutosave.setStatus` | VariableDeclaration | React state setter for status. Schedules a rerender, not a server mutation. | `useState("")` |
| `DraftAutosave.baseVersion` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `JSON.stringify(job.config)` |
| `DraftAutosave.draftVersion` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `JSON.stringify(design)` |
| `DraftAutosave.callback@142` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.current` | VariableDeclaration | Async cleanup guard against stale/unmounted SRT updates. | `true` |
| `DraftAutosave.flush` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `() => { void fetch(`/api/projects/${job.project_id}/draft`, { method: "PUT", headers: { "Content-Type": "application/json" }, credentials: "same-origin", body: JSON.stringify({ des` |
| `DraftAutosave.callback@149` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.callback@156` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.timer` | VariableDeclaration | Polling interval handle cleared when the effect is disposed. | `setTimeout(() => { api("/library/session", undefined, "POST") .then(() => api<{ saved: boolean }>( `/projects/${job.project_id}/draft`, undefined, "PUT", JSON.stringify({ design, b` |
| `DraftAutosave.callback@159` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.callback@161` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.saved` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `boolean` |
| `DraftAutosave.callback@169` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.result` | Parameter | Result of the operation/parser/API named by its assignment. | `` |
| `DraftAutosave.callback@177` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `DraftAutosave.callback@184` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `module.BrandTemplates` | FunctionDeclaration | Name, save and apply reusable visual branding while retaining episode audio/captions/title. | `{ job, token, dirty, disabled, onChange, }: { job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.token` | Parameter | Secret authentication value held in memory and sent in X-Job-Token. | `{ job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.dirty` | Parameter | Whether draft settings/text differ from the saved version. | `{ job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.onChange` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ job: Job; token: string; dirty: boolean; disabled: boolean; onChange: (job: Job) => void; }` |
| `BrandTemplates.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `BrandTemplates.token` | PropertySignature | Secret authentication value held in memory and sent in X-Job-Token. | `string` |
| `BrandTemplates.dirty` | PropertySignature | Whether draft settings/text differ from the saved version. | `boolean` |
| `BrandTemplates.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `BrandTemplates.onChange` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(job: Job) => void` |
| `BrandTemplates.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `BrandTemplates.name` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState("")` |
| `BrandTemplates.setName` | VariableDeclaration | React state setter for name. Schedules a rerender, not a server mutation. | `useState("")` |
| `BrandTemplates.status` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState("")` |
| `BrandTemplates.setStatus` | VariableDeclaration | React state setter for status. Schedules a rerender, not a server mutation. | `useState("")` |
| `BrandTemplates.items` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState<{ id: string; title: string }[]>([])` |
| `BrandTemplates.setItems` | VariableDeclaration | React state setter for items. Schedules a rerender, not a server mutation. | `useState<{ id: string; title: string }[]>([])` |
| `BrandTemplates.id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `BrandTemplates.title` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `BrandTemplates.selected` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState("")` |
| `BrandTemplates.setSelected` | VariableDeclaration | React state setter for selected. Schedules a rerender, not a server mutation. | `useState("")` |
| `BrandTemplates.error` | VariableDeclaration | Safe explanatory failure text; must not expose secrets or raw stderr. | `useState("")` |
| `BrandTemplates.setError` | VariableDeclaration | React state setter for error. Schedules a rerender, not a server mutation. | `useState("")` |
| `BrandTemplates.working` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(false)` |
| `BrandTemplates.setWorking` | VariableDeclaration | React state setter for working. Schedules a rerender, not a server mutation. | `useState(false)` |
| `BrandTemplates.refresh` | FunctionDeclaration | Reload local brand-template summaries through the library session. | `` |
| `BrandTemplates.refresh.data` | VariableDeclaration | Payload being parsed/transferred; validate before trusting fields. | `await api<{ id: string; title: string }[]>("/templates")` |
| `BrandTemplates.refresh.id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `BrandTemplates.refresh.title` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `BrandTemplates.refresh.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@228` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.run` | FunctionDeclaration | Wrap subtitle operations with busy/error feedback. | `action: () => Promise<void>` |
| `BrandTemplates.run.action` | Parameter | POST one authenticated operation and replace the local job snapshot. | `() => Promise<void>` |
| `BrandTemplates.run.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@258` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@263` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@264` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.created` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await api<{ id: string }>( `/jobs/${job.id}/templates`, token, "POST", JSON.stringify({ title: name.trim() \|\| job.config.title }), )` |
| `BrandTemplates.id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string` |
| `BrandTemplates.callback@284` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@287` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.item` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@296` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `BrandTemplates.callback@297` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

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
| `SubtitleReview.callback@25` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.current` | VariableDeclaration | Async cleanup guard against stale/unmounted SRT updates. | `true` |
| `SubtitleReview.srt` | PropertySignature | SRT under review; editing intentionally discards word alignment. | `string` |
| `SubtitleReview.callback@30` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.data` | Parameter | Payload being parsed/transferred; validate before trusting fields. | `` |
| `SubtitleReview.callback@36` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@37` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.run` | FunctionDeclaration | Wrap subtitle operations with busy/error feedback. | `action: () => Promise<void>` |
| `SubtitleReview.run.action` | Parameter | POST one authenticated operation and replace the local job snapshot. | `() => Promise<void>` |
| `SubtitleReview.run.e` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.dirty` | VariableDeclaration | Whether draft settings/text differ from the saved version. | `srt !== original` |
| `SubtitleReview.callback@77` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@78` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@121` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@128` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@129` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.next` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `await api<Job>( `/jobs/${job.id}/subtitles`, token, "PUT", JSON.stringify({ srt }), )` |
| `SubtitleReview.callback@147` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@147` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@156` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleReview.callback@157` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

## frontend/src/SubtitleTimeline.tsx

| Symbol and scope | Kind | Explanation | Signature / initializer excerpt |
| --- | --- | --- | --- |
| `module.EditableCue` | InterfaceDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `EditableCue.start` | PropertySignature | Start time in seconds; in multipart callbacks, byte-slice start index. | `number` |
| `EditableCue.end` | PropertySignature | Release transient drag state and hide alignment guides. | `number` |
| `EditableCue.text` | PropertySignature | Subtitle/title text; escape before ASS insertion and never translate user content. | `string` |
| `module.parseTimeline` | FunctionDeclaration | Parse draft SRT intervals for editing; final validation remains on the server. | `srt: string` |
| `parseTimeline.srt` | Parameter | SRT under review; editing intentionally discards word alignment. | `string` |
| `parseTimeline.callback@15` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `parseTimeline.block` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `parseTimeline.lines` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `block.split(/\r?\n/)` |
| `parseTimeline.index` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `lines.findIndex((line) => line.includes("-->"))` |
| `parseTimeline.callback@17` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `parseTimeline.line` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `parseTimeline.match` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `lines[index].match( /(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)/, )` |
| `parseTimeline.v` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `match.slice(1).map(Number)` |
| `module.timelineSrt` | FunctionDeclaration | Serialize cue edits back into millisecond-precision SRT. | `cues: EditableCue[]` |
| `timelineSrt.cues` | Parameter | Ordered subtitle intervals with optional estimated word timing. | `EditableCue[]` |
| `timelineSrt.stamp` | FunctionDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `value: number` |
| `timelineSrt.stamp.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `timelineSrt.stamp.ms` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.max(0, Math.round(value * 1000))` |
| `timelineSrt.callback@42` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `timelineSrt.cue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `timelineSrt.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `module.SubtitleTimeline` | FunctionDeclaration | Seek audio by cue and edit caption text/timestamps, keeping the raw SRT synchronized. | `{ job, srt, onChange, disabled, }: { job: Job; srt: string; onChange: (srt: string) => void; disabled: boolean; }` |
| `SubtitleTimeline.job` | Parameter | Temporary episode with metadata, files, approvals and cancellation resources. | `{ job: Job; srt: string; onChange: (srt: string) => void; disabled: boolean; }` |
| `SubtitleTimeline.srt` | Parameter | SRT under review; editing intentionally discards word alignment. | `{ job: Job; srt: string; onChange: (srt: string) => void; disabled: boolean; }` |
| `SubtitleTimeline.onChange` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `{ job: Job; srt: string; onChange: (srt: string) => void; disabled: boolean; }` |
| `SubtitleTimeline.disabled` | Parameter | Combined gate for busy, active or unavailable episodes. | `{ job: Job; srt: string; onChange: (srt: string) => void; disabled: boolean; }` |
| `SubtitleTimeline.job` | PropertySignature | Temporary episode with metadata, files, approvals and cancellation resources. | `Job` |
| `SubtitleTimeline.srt` | PropertySignature | SRT under review; editing intentionally discards word alignment. | `string` |
| `SubtitleTimeline.onChange` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `(srt: string) => void` |
| `SubtitleTimeline.srt` | Parameter | SRT under review; editing intentionally discards word alignment. | `string` |
| `SubtitleTimeline.disabled` | PropertySignature | Combined gate for busy, active or unavailable episodes. | `boolean` |
| `SubtitleTimeline.audio` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useRef<HTMLAudioElement>(null)` |
| `SubtitleTimeline.time` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(0)` |
| `SubtitleTimeline.setTime` | VariableDeclaration | React state setter for time. Schedules a rerender, not a server mutation. | `useState(0)` |
| `SubtitleTimeline.page` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `useState(0)` |
| `SubtitleTimeline.setPage` | VariableDeclaration | React state setter for page. Schedules a rerender, not a server mutation. | `useState(0)` |
| `SubtitleTimeline.cues` | VariableDeclaration | Ordered subtitle intervals with optional estimated word timing. | `parseTimeline(srt)` |
| `SubtitleTimeline.pageSize` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `20` |
| `SubtitleTimeline.pages` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.max(1, Math.ceil(cues.length / pageSize))` |
| `SubtitleTimeline.currentPage` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `Math.min(page, pages - 1)` |
| `SubtitleTimeline.update` | FunctionDeclaration | Replace one editable cue field and serialize the new SRT draft. | `index: number, key: keyof EditableCue, value: string \| number` |
| `SubtitleTimeline.update.index` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
| `SubtitleTimeline.update.key` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `keyof EditableCue` |
| `SubtitleTimeline.update.value` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string \| number` |
| `SubtitleTimeline.update.next` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `cues.map((cue, i) => i === index ? { ...cue, [key]: value } : cue, )` |
| `SubtitleTimeline.update.callback@73` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.update.cue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.update.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `SubtitleTimeline.callback@86` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@94` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.cue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.i` | Parameter | Zero-based iteration index local to the current loop. | `` |
| `SubtitleTimeline.callback@104` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@114` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.cue` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.j` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.index` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `currentPage * pageSize + j` |
| `SubtitleTimeline.callback@122` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@125` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@140` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@153` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@164` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@172` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@172` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@177` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.callback@177` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `SubtitleTimeline.n` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |

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
| `Design.output_format` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `"landscape" \| "portrait" \| "square"` |
| `Design.logo_x` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number \| null` |
| `Design.logo_y` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number \| null` |
| `Design.logo_scale` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `number` |
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
| `Job.project_id` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string \| null` |
| `Job.archive_error` | PropertySignature | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `string \| null` |
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
| `logoStyle.custom` | VariableDeclaration | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `design.logo_x != null && design.logo_y != null` |
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
| `TypographyControls.callback@124` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@140` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@158` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@169` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@173` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@189` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@200` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@204` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@220` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@230` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@236` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.id` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.label` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@252` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.e` | Parameter | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
| `TypographyControls.callback@264` | ArrowFunction | Scope-local value defined by the exact assignment/type excerpt below; not a separate persisted setting. | `` |
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
| `selectWords.end` | VariableDeclaration | Release transient drag state and hide alignment guides. | `Math.min(duration,b+offset)` |
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
| `main.begin` | VariableDeclaration | Capture a pointer and the original output coordinates before starting a drag/resize. | `Math.max(0,core-5)` |
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

