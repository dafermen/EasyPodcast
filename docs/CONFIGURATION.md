# Configuration reference

Only the backend reads .env at the repository root. Pydantic Settings also reads environment variables. Never commit .env. Defaults below come from backend/app/config.py; actual overrides may differ. A backend restart is needed after server configuration changes and interrupts temporary jobs. Durable library snapshots can be reopened afterward.

| Variable | Default | Meaning |
| --- | --- | --- |
| FFMPEG | ffmpeg | Native executable name/path used for normalization and rendering |
| FFPROBE | ffprobe | Native executable name/path used to inspect actual media |
| NODE | node | Runtime for the local transcription worker |
| TRANSCRIPTION_CACHE | ~/.cache/easypodcast/models | Persistent model files; separate from episode cleanup |
| TRANSCRIPTION_ALLOW_DOWNLOAD | true | Allow first-use Hugging Face model downloads |
| OPENAI_API_KEY | empty | Optional backend-only provider secret |
| IMAGE_MODEL | empty | Explicit account-accessible image model; no automatic paid model choice |
| IMAGE_SIZE | 1536x1024 | Existing optional provider request size; verify selected model support |
| IMAGE_QUALITY | medium | Existing optional provider quality argument |
| LIBRARY_ROOT | ~/.easypodcast/library | Private durable SQLite library and project/template media; initially empty or an existing marked library |
| TEMP_ROOT | OS temporary directory/easypodcast | Exclusive initially empty managed root; not the repository or a shared media folder |
| MAX_AUDIO_BYTES | 1073741824 | Maximum audio upload bytes (1 GiB) |
| MAX_SRT_BYTES | 5242880 | Maximum SRT upload bytes (5 MiB) |
| MAX_IMAGE_BYTES | 20971520 | Maximum bytes per background/logo input (20 MiB) |
| MAX_PIXELS | 25000000 | Decoded image pixel limit |
| MAX_DURATION | 7200 | Maximum audio duration in seconds; not a performance guarantee |
| TTL_SECONDS | 86400 | Idle/completed retention in seconds; reset after a completed operation |
| FAILURE_TTL_SECONDS | 900 | Failed/cancelled retention in seconds |
| ACTIVE_TTL_SECONDS | 14400 | Maximum active operation lifetime in seconds |
| QUEUE_SIZE | 2 | Pending operations, excluding the one active worker; allowed 1–8 |
| MAX_JOBS | 8 | In-memory capacity; allowed 1–100 |
| MIN_FREE_BYTES | 536870912 | Minimum free disk space floor; export has additional preventive budgeting |
| ALLOWED_ORIGINS | localhost and 127.0.0.1 on ports 5173/8000 | JSON list of permitted browser origins; no wildcard |

Browser preferences: easypodcast-language is en/es, default en; easypodcast-theme is classic/studio, default studio. Explicit stored preferences win. They are not .env fields, API settings or Design fields. Job tokens remain in memory.

Episode parameters are documented in DESIGN_CONTROLS.md and generated /openapi.json. Fields omitted from an imported Design receive model defaults. Invalid values, NaN and unexpected fields are rejected.
