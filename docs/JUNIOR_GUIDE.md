# Learning software development with EasyPodcast

This guide assumes you know basic variables, functions and loops, but are learning how a real application connects them. Work through it in order, then use CODE_REFERENCE.md to look up every named unit and scoped variable. CONFIGURATION.md explains environment settings; DESIGN_CONTROLS.md explains all episode fields.

## 1. Understand the three runtimes

React/TypeScript runs in the browser and manages what you see. Python/FastAPI runs a local HTTP server and owns temporary jobs. Node runs a separate local Whisper inference worker. FFmpeg is another native executable launched by Python. These are separate processes: changing a React variable does not directly mutate Python memory.

A variable is a named reference to a value. A function groups an operation and receives parameters. A class groups data/behavior; Job is an instance holding an episode, while Design is a Pydantic model that validates settings. A type/interface in TypeScript helps the developer before build time; Pydantic checks real untrusted requests at runtime.

## 2. Follow one upload

Open frontend/src/main.tsx and find upload. The form event provides File objects. FormData packages separate binary parts; a large audio file should not be base64 encoded into JSON. api.ts fetches /api/jobs, adding authentication only after a token exists. The same-origin path works through Vite's development proxy or FastAPI's compiled frontend.

In main.py, create_job enforces a single upload slot. receive_files in uploads.py reads body chunks and writes controlled names while counting bytes. Rejecting size only after accepting an entire huge file would be too late. Uploaded filenames and MIME declarations are not trusted paths or proof of media format.

validate_audio uses FFprobe to inspect actual streams/duration. normalize_image decodes images with Pillow. parse_srt checks UTF-8, ordered time intervals and visible text. make_job creates an ID/token and places a Job in Store.jobs. The HTTP response becomes React's job and design state.

## 3. Learn React state from the editor

The tuple `[design, setDesign]` contains a value for this render and a function that schedules the next render. change copies the previous object with one changed field, sets dirty and clears saved confirmation. It does not contact the API. save sends the entire design, waits for server validation and clears dirty only after success. This explains why a failed save must not enable Continue.

job is a server snapshot; design is an editable draft. step selects the screen. busy tracks a short HTTP action; active tracks a longer queued operation. unavailable means the job was lost or expired. revision changes artifact URLs to avoid showing an old cached preview. token is never written to browser preference storage. Read the App state table in CODE_REFERENCE.md while tracing these names.

Effects start polling, move heading focus and clean up timers. Cleanup guards stop stale promises from changing an unmounted/replaced view. Polling every 1.5 seconds is observation, not a render request. A browser rerender is unrelated to FFmpeg rendering a video.

## 4. Separate validation, state and expensive work

Design validates colors/enums/numeric bounds. safe_layout rejects overlap. Server validation remains required even if the browser uses min/max controls: a different HTTP client can bypass the page.

Enqueueing copies the design. One worker consumes the queue and runs FFmpeg/Node outside the event loop. Async allows waiting for I/O without blocking other requests; it does not make CPU-intensive work free. Threads drain process pipes so stdout/stderr cannot fill and deadlock the child. A lock protects shared job updates.

Subprocess calls use argument lists with shell=False. A string joined into a shell command could execute injected syntax. Filtergraphs are another language, so their values are allowlisted and title/subtitle text is written to escaped ASS instead of interpolated as arbitrary filter commands.

## 5. Understand subtitle time and text

An SRT cue has start/end seconds and text. A preview beginning at second 5 clips a cue from 4–8 to 0–3: intersect with the selected segment before shifting. Simply subtracting five would create a negative start. clip_cues also tracks word offsets so highlighting remains aligned when the clip begins inside a phrase.

ASS adds fonts, outline, alignment and position at 1920 × 1080. make_ass builds the document; libass draws it. wrap_text measures the real selected TTF, not a guessed character count. escape_ass prevents user text from becoming override commands. Uploaded/edited SRT lacks trustworthy word timing, so it uses normal subtitles.

## 6. Understand output and cleanup

showwaves/showfreqs analyze an audio branch. Another branch feeds AAC so visualizer sensitivity does not change the sound. A partial output is published only after FFprobe validates codec/resolution/fps/duration. Watching a real preview is necessary because the CSS canvas is approximate.

Downloads stream with Range support; creating a browser Blob for a long MP4 could duplicate memory use. Reader leases prevent deletion during an active response. A finally block releases the lease even after disconnect. Temporary jobs have deadlines. The separate SQLite library can now reconstruct a fresh workspace from saved media and metadata; it never serializes live threads or subprocesses.

## 7. Preferences, secrets and errors

Theme and language are browser preferences. The locale store notifies React subscribers; t translates known UI messages. Never pass user-authored SRT/title text to t. Spoken audio language belongs to transcription, not the interface selector.

Environment variables configure server tools and limits. An OpenAI key in frontend code would be visible to every browser user. A job token grants access to one temporary job; it is not a provider key. Sanitized errors explain recovery without exposing raw stderr or filesystem paths.

## 8. Read tests as executable examples

Unit tests cover pure parsing/timing/layout. API tests exercise validation and state transitions. Multimedia integration tests generate synthetic audio, render a real MP4 and inspect frames. A fake provider tests the contract without billing but cannot prove account access. A passing Linux CI run does not prove native macOS behavior.

Try these exercises in a branch:

1. Add a coral design preset. Update only Design draft values; preserve Save and Preview approval. Test that the backend still rejects invalid colors.
2. Test clipping Cue(20,30) with start=5, duration=20. Expected relative interval is 15–20.
3. Explain why two Uvicorn workers break an in-memory registry: requests can reach a process that does not own the job.
4. Add one UI help message in both languages, then switch language during an unsaved draft and confirm the draft survives.
5. Inject a timeout provider in a test. Verify failed state and retained input files without calling a paid API.

When stuck, identify the owner of the value, its units, who changes it and how it is cleaned up. Then follow its definition and callers in CODE_REFERENCE.md.

## 9. Learn persistence from the project library

Read library.py next to jobs.py. A live Job contains things that cannot be serialized safely (thread events, subprocess handles and a secret token). checkpoint explicitly extracts portable fields and copies only allowlisted changed files. SQLite commits metadata; a temporary file plus replace publishes each copied medium. This separation explains why durable data survives workspace cleanup without pretending the running encoder survives a restart.

A recovery draft is distinct from the committed Design. Its base version prevents an old network request from overwriting a newer explicit save. DraftAutosave depends on serialized content versions, not each new object returned by polling; otherwise an identical status refresh would resubmit the draft repeatedly. Preflight similarly checks meaningful state changes rather than every polling tick.

Follow frameSize/canvasDelta/logoBox in CanvasEditor.tsx to see coordinate transforms: a 50-pixel pointer move on a half-size canvas is 100 output pixels. Compare those results with the FFmpeg graph and ASS resolution. Read SubtitleTimeline.tsx for parsing cue intervals, seeking an HTML audio element and writing corrected SRT back to the existing validated API.

## Follow a portable project from browser to disk

1. Start at LibraryTools.tsx: preparing a download calls a JSON endpoint; clicking the returned anchor streams a file through the browser. It does not allocate the MP4/ZIP as a JavaScript Blob.
2. Read library_routes.attach: the router requires a local HttpOnly session and shares the existing Origin guard. A semaphore limits expensive package work; a ticket identifies private staging, not a filesystem path.
3. Read packages.build: freeze archived files under a lock, then release the lock before hashing and writing the ZIP. Hard links keep old file versions alive when a checkpoint atomically replaces the library file. Copying is the cross-filesystem fallback.
4. Read inspect_package: a filename is untrusted input. Fixed UUID paths, filename allowlists, byte budgets, hashes and real media inspection are separate checks. A checksum proves the bytes match the manifest; it does not prove who created them.
5. Read install: allocate fresh identities inside a transaction. Record every newly created directory so an exception removes only those incomplete copies. Existing projects remain untouched.
6. Read transfers.TransferManager: a lease prevents expiry from deleting a file while another request consumes it. Expiry and cancellation clean temporary staging; neither prunes the durable library.

## Understand subtitle recovery concurrency

The textarea can temporarily contain invalid SRT. A recovery draft stores this raw string; parsed cues remain unchanged until explicit save succeeds. The saved SRT SHA-256 identifies the baseline content. The integer generation changes on save/discard, so a delayed request cannot resurrect a discarded draft even when the saved text has not changed. This is optimistic concurrency: reject stale work instead of silently overwriting newer work. drafts.ts registers save functions from mounted editors and awaits them before switching projects. Page-close requests remain best-effort; an acknowledged save is the reliable evidence.

Try the isolated test_portable.py fixtures before modifying protocol rules. Add a malformed archive case, verify it returns a safe rejection and confirm the existing library count/media are unchanged. Never point destructive tests at a user's real library.
