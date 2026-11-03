# EasyPodcast

Aplicación web local, frontend React/TypeScript y backend Python/FastAPI con FFmpeg nativo.
Lee README.md, docs/ARCHITECTURE.md y docs/IMPLEMENTATION_STATUS.md antes de modificar.
Documentación e interfaz en español; código y rutas API en inglés.
Mantén docs/IMPLEMENTATION_STATUS.md con evidencia real. No declares probado macOS sin ejecutarlo allí.
Un solo proceso Uvicorn y un worker de render. Bind 127.0.0.1.
Nunca incluyas claves, medios personales, temporales o resultados en Git.
No hagas llamadas pagadas en tests ni publiques videos o despliegues automáticamente.
La licencia del código propio es MIT, elegida por el propietario. Conserva LICENSE y los avisos/licencias de terceros; no cambies la licencia sin instrucción del propietario. No borres medios fuera de la raíz temporal administrada.
Verificación: backend `python -m pytest -q`; frontend `npm test` y `npm run build`.
