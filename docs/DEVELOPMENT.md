# Developer workflow

Start with README installation, then read JUNIOR_GUIDE.md and CODE_REFERENCE.md. The backend resolves .env relative to the repository, not the current shell directory. Run one Uvicorn worker only.

## Development servers

Run scripts/start.ps1 (Windows) or scripts/start.sh (macOS) for the backend on 8000. In another terminal:

```powershell
npm.cmd --prefix frontend run dev
```

Vite serves 127.0.0.1:5173 and proxies /api to 8000. A frontend-only production build needs no backend restart. Backend changes require restart, which removes temporary episodes. A browser refresh also loses the current in-memory token; download work first.

## Editing conventions

Use English identifiers, source comments and documentation. Localize UI strings in English and Spanish, including labels, accessible names, errors and progress. Keep technical enums, route names and JSON keys stable. Add entries to frontend/src/locales/en.json and call t only on UI messages. See LOCALIZATION.md.

Prefer explicit code over empty abstractions. Separate validation from subprocess execution and lifecycle. Explain invariants, units and side effects in docstrings; the source reference lists parameters and variables by scope. Regenerate it with `python scripts/build_code_reference.py` after symbol changes. Never edit generated sections by hand.

## Checks

```powershell
.\.venv\Scripts\python.exe -m pytest backend/tests -q
.\.venv\Scripts\python.exe -m ruff check backend/app backend/tests --config backend/pyproject.toml
npm.cmd --prefix frontend test
npm.cmd --prefix frontend run format:check
npm.cmd --prefix frontend run build
npm.cmd --prefix transcription test
.\.venv\Scripts\python.exe scripts/doctor.py
```

Use npm run format for frontend formatting. Dependency locks are committed. Do not add global runtime dependencies. Regenerate the appropriate lock when dependencies change. CI installs dependencies from locks and runs Linux checks.

## Debugging

First check /api/health, then /api/capabilities or scripts/doctor.py. Missing FFmpeg filters cannot be fixed by changing React. Use /docs and /openapi.json to inspect request schemas. Use scripts/render_cli.py to isolate the media pipeline from browser state. Never log .env, tokens, full provider responses or user media. A 404/410 can mean an expired/deleted job, restart or invalid session, not a file-size limit.

## Adding a feature

1. Identify which layer owns it and define its validated contract.
2. Preserve defaults for older design JSON files.
3. Implement server validation before exposing a control.
4. Show feedback and invalidate stale approvals as needed.
5. Localize labels and add a meaningful behavior test.
6. If rendering changes, verify an actual synthetic MP4, not only a mocked call.
7. Update docs/status and regenerate the code reference.

For a provider, implement ImageProvider.generate_background and inject fakes in tests. Never automatically retry a potentially billable request. For macOS, create fresh dependencies and run the multimedia suite before claiming validation.
