"""Run from repository root with its virtualenv Python."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from app.media import capabilities

result = capabilities()
print(json.dumps(result, indent=2, ensure_ascii=False))
raise SystemExit(0 if result["render_ready"] else 1)
