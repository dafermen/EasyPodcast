# Desarrollo

Sigue README para instalar. El backend resuelve `.env` desde la raíz del repositorio, independiente de la carpeta actual. Los scripts de inicio sitúan el proceso en `backend` para importar app. Nunca ejecutar varios workers. El frontend usa Vite en 5173 con proxy `/api` a 8000.

## Organización y estilo

No crear abstracciones vacías. Validación separada de ejecución multimedia y ciclo de vida. Español en UI/documentación; inglés en identificadores. Textos comunes en `frontend/src/text.ts`; algunos textos del asistente permanecen junto al componente y su extracción completa es una mejora pendiente.

Usa `python -m ruff check app tests` y `python -m ruff format app tests` desde backend. TypeScript se comprueba con `npm run build`; pruebas con `npm test`. El repositorio no exige lint frontend independiente. No instalar paquetes globales para la aplicación. `requirements.lock` fija resolución; `package-lock.json` fija npm. Al cambiar dependencias regenera ambos y prueba.

Frontend: `npm run format` aplica Prettier y `npm run format:check` verifica formato. La compilación no necesita acceso a APIs externas.

## Extensiones

Un preset debe generar un Design validado, sin filtros arbitrarios. Añade la opción UI, comprueba límites y prueba con FFmpeg real. Un proveedor implementa `ImageProvider.generate_background(design, destination)` y produce PNG normalizado; inyecta un falso solo en tests. No registrar prompts/secretos ni reintentar cobros sin acción del usuario.

## Depuración

`scripts/doctor.py` inspecciona ejecutables, encoders, filtros y fuente sin rutas ni claves en salida. `/docs` ofrece OpenAPI. Usa el pipeline CLI para aislar fallos de React. La respuesta API oculta stderr y rutas del sistema. No actives access logs con tokens en URL (el diseño no los necesita).

Windows: invocar `npm.cmd` evita la política de ejecución de npm.ps1. FFmpeg se lanza con shell=False y rutas controladas; cancelación usa taskkill /T /F. macOS: grupo de procesos nuevo, SIGTERM y SIGKILL de respaldo. No usar rutas de unidad dentro de filtergraphs. Los scripts shell se guardan LF.

## Continuar en el Mac

Clona el repositorio y crea un entorno virtual nuevo; nunca copies `.venv` o `node_modules` entre OS. Instala FFmpeg nativo, ejecuta doctor, tests y build. El código no necesita Xcode. Repite integración multimedia y revisión visual, registra versiones y resultados en IMPLEMENTATION_STATUS. No declares compatibilidad comprobada hasta ese momento.
