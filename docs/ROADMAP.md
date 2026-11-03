# Fases y tareas

Cada tarea debe distinguir código existente de comportamiento verificado. La columna estado se mantiene en IMPLEMENTATION_STATUS.

| Fase | Actividades | Aceptación |
|---|---|---|
| 0 Preparación | repositorio, entorno, docs, diagnóstico, frontend/backend y locks | health/capabilities y build reales |
| 1 Primer video | validación audio/SRT/imagen, ASS, CLI, FFmpeg y fixture sintético | MP4 decodificable y FFprobe válido |
| 2 Flujo web | cargas streaming, tokens, cola, polling, cancelación, descarga, TTL | recorrido desde navegador |
| 3 Diseño | onda/barras, título/logo, subtítulos, fragmentos con tiempos ajustados | respuesta visual y prueba corta revisada |
| 4 IA opcional | SDK oficial, proveedor, errores, aprobación y reutilización | contrato falso probado; llamada real solo con configuración del usuario |
| 5 Robustez | seguridad local, limpieza, CI, pruebas, docs y benchmark | evidencia, límites y pendientes explícitos |

Trabajo posterior verificable: probar macOS, realizar generación real controlada si el usuario la solicita/configura, medir 30–60 minutos con CPU/RAM/disco, ampliar pruebas de cierres abruptos y diversos decodificadores, extraer todos los textos UI, mejorar ajuste de subtítulos densos y dividir App en componentes al crecer. No añadir funcionalidades fuera de alcance para llenar el roadmap.
## Próximo bloque · Claridad después de guardar diseño (2026-11-03)

Estado: pendiente, solicitado por el usuario; no implementado todavía.

Problema observado: después de Guardar diseño, el usuario no descubre que debe pulsar Aprobar fondo y continuar. La tarjeta opcional de IA separa ambas acciones y el botón siguiente tiene poca jerarquía visual.

Propuesta recomendada:
- Mostrar confirmación persistente y accesible: «Diseño guardado. Revisa el fondo y pulsa Aprobar fondo y continuar».
- Cambiar Guardar diseño por «✓ Diseño guardado» tras guardar correctamente.
- Dar a «Aprobar fondo y continuar →» fondo verde sólido y texto blanco cuando esté habilitado; no depender solo del color.
- Agrupar las acciones de guardar y continuar para que la tarjeta opcional de IA no interrumpa el recorrido. Conservar acceso claro a generación de imágenes.
- No avanzar ni aprobar automáticamente. Si hay cambios sin guardar o una operación activa, mantener el bloqueo y explicar qué falta; si falla el guardado, no mostrar éxito.

Aceptación: tras guardar correctamente, el siguiente paso se identifica por texto y jerarquía visual; funciona con teclado, foco visible y anuncio accesible. Confirmar el recorrido con imagen propia y sin proveedor IA, además de la generación opcional.
