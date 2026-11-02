#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT/backend"
exec "$PROJECT_ROOT/.venv/bin/python" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --no-access-log
