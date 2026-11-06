# Testing and verification

## Required commands

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
.\.venv\Scripts\python.exe -m ruff check backend/app backend/tests --config backend/pyproject.toml
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run build
npm.cmd --prefix transcription test
.\.venv\Scripts\python.exe scripts/doctor.py
.\.venv\Scripts\python.exe scripts/build_code_reference.py
```

On macOS/Linux use .venv/bin/python and npm. Do not make paid provider calls during tests. Use synthetic fixtures; do not commit personal recordings. Backend tests isolate managed roots and use a fake image provider. Real FFmpeg renders exercise codecs, subtitle layout, typography, title position and logo placement. Frontend tests check state/approval/API contracts, language/theme preferences and storage failure. Node tests cover window-word selection and silence detection.

## Levels of confidence

Pure tests prove parsing and math. API tests prove request/state contracts. A rendered/decoded synthetic MP4 proves the tested media pipeline. Browser review proves the observed interaction. A mocked provider does not prove billing/authentication/quality; a CSS preview does not prove final video layout. Keep these distinctions in IMPLEMENTATION_STATUS.md.

Current baseline before bilingual changes: 97 backend and 18 frontend tests passed in Windows; fonts were rendered in both weights. Historical Node suite: two tests. The current change's actual results are recorded after execution in IMPLEMENTATION_STATUS.md. Starlette currently emits a testclient/httpx deprecation warning; it is not a failing test.

## Reproducible fixtures and benchmark

```powershell
.\.venv\Scripts\python.exe scripts\fixtures.py --output media\fixtures --seconds 26
.\.venv\Scripts\python.exe scripts\render_cli.py --audio media\fixtures\demo.wav --srt media\fixtures\demo.srt --output media\preview.mp4 --seconds 20
.\.venv\Scripts\python.exe scripts\benchmark.py --minutes 30 --output media\benchmark-30m
```

Choose a new output path; utilities avoid overwriting retained outputs. The benchmark samples process-tree RSS, CPU and managed disk usage. Existing docs/benchmarks/windows-30m.json records one 30-minute synthetic run: 720.20 seconds render wall time, 391.15 MiB peak RSS, 196.48 MiB peak managed disk and 2267.53 observed cumulative CPU seconds. It is not a statistical average or a 120-minute guarantee. Exited children can disappear from CPU samples.

## Manual review checklist

Try a fresh English/Studio browser, then Spanish and Classic; verify reload persistence without an active episode. During a synthetic episode, change UI preferences and confirm unsaved design survives. Review accessible labels, errors, status, dates and narrow-screen header wrapping. Create/import settings, save, explicitly approve background, render/review a short clip and export. Keep a screenshot of observed layout. Native macOS, screen-reader assessment, long human speech, Base inference quality, paid images and crash/disconnect stress remain separate pending checks.

## Durable studio validation (0.5.0)

The isolated library suite verifies cross-thread-safe restart/recovery, token-free snapshots, versioned draft conflicts, named media templates, independent duplication, session capacity/eviction, unknown-ID safety, retention of the only workspace copy after archive errors, reconnecting to an active render, and read-only preflight during downloads. Real synthetic renders cover landscape, portrait, square and free-position/scaled logos; a portrait input's original aspect is preserved through library/template/download paths. Browser review additionally exercised recovery after a real restart, pointer drag, audio playback/seek, SRT edits and full export. Performance for large durable libraries and power-loss corruption is not implied by these tests.

## Portable library validation (0.6.0)

Synthetic isolated-library tests cover project/media/draft roundtrips, backup templates and Trash, new identities, validation-before-confirmation, owner/Origin checks, malformed/checksum/path/duplicate rejection, cancellation/budgets, rollback of failed copies, lease expiry and word timestamps. Recovery checks cover incomplete subtitle text, edit-generation conflicts, explicit discard/save and render gates. Frontend tests exercise typed purge confirmation, import review and draft flushing. Never run destructive fixture tests against a real library.
