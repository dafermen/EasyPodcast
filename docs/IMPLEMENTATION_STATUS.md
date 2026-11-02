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
- Licencia del propietario pendiente; avisos de fuente/FFmpeg documentados.

## Próximo trabajo en Mac

Clonar repositorio, instalar dependencias nativas, crear .venv, npm ci/build, doctor, pytest, pruebas frontend y recorrido de navegador. Registrar resultado y versiones; decidir después si se quiere alojamiento remoto (requiere diseño adicional).

## CI remoto verificado

GitHub Actions pasó en Ubuntu con Python 3.12 y Node 24 para el commit 581d670: doctor, 35 pruebas backend con FFmpeg real, Ruff, 5 pruebas frontend, formato y build. [Ejecución 41440870852](https://github.com/dafermen/EasyPodcast/actions/runs/41440870852). Esto verifica Linux en CI, no sustituye la prueba nativa de macOS.

