# EasyPodcast contributor instructions

Local web application: React/TypeScript frontend, Python/FastAPI backend, native FFmpeg and a local Node Whisper worker.

Read README.md, docs/ARCHITECTURE.md and docs/IMPLEMENTATION_STATUS.md before changing code. All project documentation and source comments must be in English. The interface supports English and Spanish, with English as the initial language and Studio as the initial theme. Keep existing explicit browser preferences. Code identifiers and API routes remain English.

Run one Uvicorn process with one worker and bind to 127.0.0.1. Never commit secrets, user media, model caches, temporary files or rendered videos. Do not make paid API calls in tests or publish videos/deployments automatically. Preserve the MIT license and all third-party font license notices. Delete only managed temporary workspaces and incomplete library staging files created by the app. Never automatically prune durable library projects or user originals. Backend restarts interrupt in-memory operations; durable project snapshots survive, but unsaved edits or unarchived older-version episodes can be lost. Obtain permission before interrupting active work.

Required checks: python -m pytest backend/tests -q; python -m ruff check backend/app backend/tests --config backend/pyproject.toml; frontend npm test, npm run format:check and npm run build; transcription npm test when relevant. Update docs/IMPLEMENTATION_STATUS.md with observed evidence; never claim native macOS validation without running there. Run python scripts/build_code_reference.py when source symbols change.
