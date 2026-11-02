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
