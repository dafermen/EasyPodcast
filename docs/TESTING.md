# Pruebas y evidencia

Ejecuta desde la raíz con el Python del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests -q
.\.venv\Scripts\python.exe -m ruff check backend\app backend\tests --config backend\pyproject.toml
Set-Location frontend
npm.cmd test
npm.cmd run build
npm.cmd audit --audit-level=moderate
```

En macOS cambia a `.venv/bin/python` y `npm`. FFmpeg/FFprobe deben estar instalados; la suite multimedia no se sustituye por mocks cuando faltan filtros. CI instala FFmpeg en Ubuntu y ejecuta las mismas verificaciones. Su ejecución remota debe comprobarse por separado.

## Verificado en esta laptop Windows · 2026-11-02

- **35 pruebas backend pasaron**: UTF-8/BOM, SRT inválido, solapamientos, escape ASS, clipping por ambos extremos, límites/configuración/layout, tokens/origen/Host, límites de carga incremental sin Content-Length, formatos falsos, imágenes, expiración con lectores, limpieza de reinicio, cola acotada, proveedor falso y contrato del SDK sin red, errores de proveedor, cancelación de un proceso real y reintento.
- Integración FFmpeg real para waveform y spectrum: salida 1920×1080/30 fps/H.264/AAC/yuv420p; tolerancia de duración 0,25 s. Comparación de cuadros entre silencio y tono, retorno a silencio, subtítulos presentes/ausentes y fondo sin rectángulo negro. Audio AAC decodificado: RMS bajo en silencio y alto en tono.
- **5 pruebas frontend pasaron**: cabecera de token, URLs sin token, errores accionables, estados de reintento, carga/diseño con IA ausente y error de conexión. El submit del formulario se dispara explícitamente en jsdom para aislar diferencias de validación HTML nativa; el navegador real cubrió el recorrido completo.
- Build TypeScript/Vite correcto; Ruff correcto; npm audit sin vulnerabilidades reportadas en la resolución instalada.
- Navegador real: carga de WAV/SRT sintéticos de 26 s, título personalizado, aprobación de fondo, prueba de 20 s desde segundo 2, lectura multimedia readyState=4 sin error, aprobación y exportación de 26 s. Descarga real en `Downloads/video.mp4`, comprobada con FFprobe. Captura en `docs/screenshots/web.png`.

Advertencia no bloqueante de la versión instalada de Starlette: TestClient anuncia futura migración de httpx a httpx2; la suite actual usa httpx y pasa. No se realizó reproducción auditiva humana ni prueba con una grabación personal. La corrección del audio se verificó por decodificación y métricas del tono sintético.

## Benchmark manual reproducible

```powershell
.\.venv\Scripts\python.exe scripts\benchmark.py --minutes 30 --output media\benchmark-30m
```

Requiere psutil (incluido en dependencias de desarrollo/lock). Genera silencio y tono alternados, SRT con acentos/llaves/barra, fondo local y render 1080p, CRF 21, preset veryfast, dos threads de encoder y dos de filtros. Guarda `benchmark.json` con tiempo, RAM RSS agregada, CPU acumulada observada y pico de disco administrado. Los resultados medidos se conservan en `docs/benchmarks/windows-30m.json` al completar la ejecución. No extrapolar a otros equipos o a 120 minutos.

Ejecución completada en Windows: 30 min de audio → 720,20 s de render; 391,15 MiB pico RSS agregado; 196,48 MiB pico de disco administrado (incluye entradas y salida); 2.267,53 s CPU acumulada máxima observada por muestreo. CPU no equivale a tiempo de pared ni es una medida del sistema completo; los procesos hijos que terminan pueden desaparecer antes de la última muestra. Resultado de una ejecución, no promedio estadístico.

## Pendientes de verificación externa

macOS nativo, llamada pagada con credenciales OpenAI, episodios de voz reales y 60–120 minutos, caracteres que requieran fuentes adicionales, cierre abrupto del OS, desconexión de descargas bajo carga y evaluación de accesibilidad con lector de pantalla. CI remoto se registra en IMPLEMENTATION_STATUS tras observar su resultado. No hay afirmación de preparación para Internet.
