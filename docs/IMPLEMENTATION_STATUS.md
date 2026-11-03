## Flujo de diseño · 2026-11-03

- Diseño comienza con la elección Configurar manualmente o Importar un diseño JSON.
- El JSON carga los ajustes y permite revisarlos; audio, subtítulos, fondo y logo se cargan aparte. Un archivo inválido no reemplaza el diseño actual.
- Guardar y continuar están juntos. Tras guardar aparece la confirmación y el botón verde «Aprobar fondo y continuar →». Los cambios pendientes bloquean continuar; la aprobación sigue siendo explícita.
- Verificación: 15 pruebas frontend y compilación TypeScript/Vite correctas en Windows. Cambio exclusivo del frontend, sin reinicio del backend.

## Conservación de episodios · 0.4.1 (2026-11-03)

Se amplía TTL_SECONDS de 3600 a 86400: 24 h tras creación o última operación completada. Fallos/cancelaciones siguen a 15 min y operaciones activas a 4 h. /api/capabilities expone retention. El polling renueva solo la cookie de medios hasta el vencimiento real; no prolonga el trabajo. Se mantienen borrado manual, limpieza y espera por descargas activas.

404/410 explican que el episodio pudo vencer, eliminarse, perderse en un reinicio o tener sesión inválida. La interfaz bloquea el render al detectar pérdida del trabajo, permite guardar el diseño aún en memoria como JSON y ofrece cargar otro episodio. Un clip visible puede estar en caché; no demuestra que el servidor conserve el audio. No hay persistencia entre reinicios: un trabajo ya eliminado no se restaura cambiando el límite.

---

# Estado actual · 0.4.0

Casilla Negrilla en el título y siete familias disponibles: DejaVu Sans/Serif/Mono, Nunito, Fredoka, Rounded (derivada de Quicksand, renombrada por licencia) y Poppins. Archivos Regular/Bold reales, servidos localmente, usados por medición de título, vista de composición y FFmpeg. Nuevas fuentes también en subtítulos. Licencias incluidas y JSON anterior compatible (title_bold=true por defecto).

Windows: 69 pruebas backend y 10 frontend pasaron, build correcto. Renders reales para las cuatro familias nuevas en ambos pesos; diferencia visual comprobada por píxeles en la región del título. macOS y selección estética final del usuario pendientes. La mejora de guía después de Guardar diseño continúa pendiente en ROADMAP.md y no se implementó en este bloque.

---

# Estado actual · 0.3.0

Tipografía y logo: fuente y tamaño independientes para título/subtítulos, tres familias DejaVu incluidas, seis posiciones y margen de logo. Vista previa con fuentes locales y logo; ASS/FFmpeg usan la misma configuración. Compatibilidad con JSON anteriores mediante defaults. Ver docs/DESIGN_CONTROLS.md.

Verificado en Windows: 56 pruebas backend y 9 frontend pasaron; renders reales con Serif/Mono, tamaño elegido y logos en esquinas opuestas, rutas de fuentes permitidas y límites. Navegador real: cambios de fuente, tamaños y posición, guardar y renderizar prueba con audio sintético y recursos generados. Capturas typography-controls.png y typography-render.png. macOS nativo pendiente.

---

# Estado actual · 0.2.0

## 0.2.0 · Generación local de subtítulos y resaltado

Ampliación solicitada: opción inicial audio + SRT o audio solo con transcripción local Whisper Tiny/Base. Revisión y descarga SRT, aprobación antes de Diseño, corrección básica y reintento. Resaltado de la palabra actual en amarillo configurable, con tiempos estimados del modelo. Los SRT propios/editados conservan subtítulos normales para evitar alineación inventada.

Implementación: app/transcription.py + transcription/worker.mjs independiente; no se modificó vDownloader. Modelo Tiny ya existente se copió a la caché independiente de EasyPodcast. Audio por ventanas acotadas, cola común, cancelación, timeout, progreso por segmentos y limpieza de PCM/JSON. Caché de modelos persistente fuera de Git; descargas configurables, sin llamadas pagadas.

Verificación Windows: 44 backend, 7 frontend y 2 Node pasaron; build, formato, Ruff y auditoría de dependencias correctos. Whisper Tiny real CPU q8 reconoció 11 palabras de voz sintética inglesa de 4,435 s. Flujo real audio solo → SRT → aprobación → MP4 con resaltado y limpieza pasó. Cuadros del render confirman que el amarillo cambia de palabra, incluido recorte a mitad de frase. Navegador real confirmó selección inicial, transcripción, revisión, aprobación y controles de resaltado. Se corrigió y probó una colisión entre la lectura del fondo y la del SRT.

Servicio activo comprobado: /api/health versión 0.2.0 y transcription.available=true. Capturas docs/screenshots/audio-only-flow.png, word-highlight-controls.png y word-highlight.png. Guía docs/TRANSCRIPTION.md.

Pendientes: macOS nativo, Whisper Base real y calidad/rendimiento en voz humana larga o bilingüe. El benchmark previo de 30 min mide render, no transcripción. Los tiempos por palabra son estimados; primera descarga de modelos y uso offline sin caché no se comprobaron (se reutilizó caché). No se afirma precisión perfecta ni identificación de hablantes.

---

# Estado real de implementación

Actualizado: 2026-11-02. Web local; Xcode fuera del alcance. Este archivo distingue código entregado de pruebas ejecutadas.

| Fase | Implementación | Verificación |
|---|---|---|
| 0 Preparación | repositorio, documentación, React/FastAPI, entorno, locks y doctor | Windows: arranque, build, health/capabilities reales |
| 1 Primer video | CLI, validación, ASS y render FFmpeg | MP4 reales, FFprobe y decodificación de audio/cuadros |
| 2 Flujo web | cargas streaming, trabajos, cola, tokens, polling, cancelación, Range y TTL | pruebas API y recorrido navegador con descarga |
| 3 Diseño | fondo, título/logo, onda/barras, subtítulos y prueba de hasta 20 s | ambos visualizadores, clipping, legibilidad en captura y prueba real |
| 4 IA opcional | SDK oficial detrás de proveedor, parámetros por entorno, aprobación y fallback | contrato SDK falso/errores probados; llamada real pendiente de credenciales y acción del usuario |
| 5 Robustez | límites, limpieza, protección local, tests, CI y benchmark reproducible | 35 backend + 5 frontend, build/Ruff/audit correctos; benchmark Windows de 30 min completado |

## Evidencia

Windows, Python 3.14.7, Node 24.18.0, FFmpeg 9.0.2 (Gyan, GPL/version3). Versiones Python exactas en backend/requirements.lock y npm en frontend/package-lock.json. Suite actual: 35 backend, 5 frontend, ninguna llamada pagada. Motor listo: FFmpeg, FFprobe, libx264, AAC, libass, showwaves, showfreqs, overlay, colorkey y fuente incluida. Ver docs/TESTING.md para cobertura y límites.

Recorrido web: 26 s sintéticos, prueba 20 s desde segundo 2, exportación y descarga MP4 verificadas a 1080p/30 fps/H.264/AAC. No se incluyeron medios personales. Captura real en docs/screenshots/web.png.

Benchmark real: 1.800 s de audio sintético exportados en **720,20 s (12 min)**, preset veryfast/CRF 21, pico RSS agregado **391,15 MiB**, pico de disco administrado **196,48 MiB** y CPU acumulada máxima observada **2.267,53 s**. Ocho CPU lógicas. Salida validada con FFprobe. Muestra reproducible, no garantía para otras grabaciones/equipos ni 120 min. Datos completos: docs/benchmarks/windows-30m.json.

## Limitaciones concretas

- macOS documentado, aún no ejecutado; recrear entornos y probar allí.
- IA opcional implementada, sin generación real pagada ni modelo elegido por el propietario. No se promete identidad repetible con regeneración.
- Un proceso, un worker, dos pendientes. Sin cuentas, historial, reanudación o exposición pública.
- Recargar la pestaña pierde el token de React. Reiniciar backend elimina los trabajos. Descargar primero.
- SRT denso que no cabe en dos/tres líneas se rechaza con explicación; no se modifica/trunca silenciosamente.
- Cancelar una generación externa espera respuesta/timeout, no garantiza detener cobro.
- Layout CSS aproximado; prueba FFmpeg es la referencia. Preset IA de presentadores fijo mujer izquierda/hombre derecha; no hay editor de personajes.
- Algunos textos UI permanecen en App; extracción completa y división en componentes pueden hacerse al crecer.
- Benchmark no valida voz humana, todos los codecs posibles ni 120 minutos. La revisión editorial corresponde al creador.
- Código propio bajo MIT por decisión del propietario (2026-11-03); fuentes/FFmpeg y demás terceros conservan sus licencias.

## Próximo trabajo en Mac

Clonar repositorio, instalar dependencias nativas, crear .venv, npm ci/build, doctor, pytest, pruebas frontend y recorrido de navegador. Registrar resultado y versiones; decidir después si se quiere alojamiento remoto (requiere diseño adicional).

## CI remoto verificado

GitHub Actions pasó en Ubuntu con Python 3.12 y Node 24 para el commit 581d670: doctor, 35 pruebas backend con FFmpeg real, Ruff, 5 pruebas frontend, formato y build. [Ejecución 41440870852](https://github.com/dafermen/EasyPodcast/actions/runs/41440870852). Esto verifica Linux en CI, no sustituye la prueba nativa de macOS.

Verificación visual 0.4.0: navegador real alternó negrilla, seleccionó Fredoka/Nunito y guardó el diseño. document.fonts confirmó ambos pesos/fuentes cargados localmente. Captura docs/screenshots/friendly-fonts.png. Servicio /api/health versión 0.4.0 comprobado activo.

Verificación 0.4.1: 72 pruebas backend y 12 frontend pasaron; build y formato correctos. Casos de vencimiento 410/404, límite de 24 h y cookie alineada sin renovar TTL, además de recuperación de interfaz ante 404. Servicio activo respondió retention.completed_seconds=86400, failed_seconds=900, active_seconds=14400 y survives_restart=false. No se restauró el episodio ya perdido de la captura.
