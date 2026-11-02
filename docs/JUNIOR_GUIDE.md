# Guía para aprender con EasyPodcast

## Sigue una petición real

En `frontend/src/main.tsx`, el formulario reúne objetos File en FormData. HTTP multipart permite enviar partes binarias distintas, cada una con nombre; JSON sería inadecuado para un audio grande. `src/api.ts` hace fetch al proxy `/api` y convierte errores en mensajes. React guarda Job, Design, paso y token en memoria. Cambiar un estado vuelve a renderizar la vista; no significa ejecutar FFmpeg otra vez.

`backend/app/main.py:create_job` recibe la petición. `uploads.py` lee el stream y escribe fragmentos en nombres internos mientras cuenta bytes: rechazar después de almacenar un archivo enorme llegaría tarde. Nunca se confía en el nombre del archivo o MIME. `media.py:validate_audio` usa FFprobe para inspeccionar pistas/duración reales. Pillow decodifica imágenes. `subtitles.py:parse_srt` valida UTF-8, tiempos, orden y texto.

La respuesta HTTP 201 devuelve identificador y token. TypeScript expresa el contrato en `src/types.ts`; Pydantic valida realmente en servidor. TypeScript no protege al backend de un cliente malicioso. `Design` rechaza colores que podrían introducir filtros, valores fuera de rango y campos desconocidos.

## Async y trabajo pesado

Async sirve para esperar I/O sin monopolizar el event loop; no convierte una exportación CPU en gratuita. Las inspecciones bloqueantes se envían con `asyncio.to_thread`. Renderizar se encola en `jobs.py`, cuyo worker ejecuta FFmpeg como subproceso. Un hilo lee progreso y otro stderr para evitar tuberías llenas. Cancelar termina el árbol/grupo y solo después libera el worker.

`subprocess.Popen` recibe lista de argumentos con shell=False. Concatenar texto del usuario en una línea shell permitiría comandos. Incluso sin shell, un filtergraph puede interpretar sintaxis: por eso filtros se construyen desde valores validados y textos se escriben en ASS.

## SRT, ASS y composición

SRT expresa cue inicio/final/texto. ASS añade estilos y posición. `clip_cues` toma intersección con el segmento: si un cue va de 4 a 8 segundos y la prueba empieza en 5, debe aparecer de 0 a 3. No basta con restar cinco a todo, pues produciría negativos. `make_ass` construye estilos a resolución 1920×1080. FFmpeg/libass dibuja esos textos. La UI CSS aproxima la composición y el MP4 corto permite revisarla realmente.

showwaves y showfreqs consumen muestras de audio; asplit conserva otra rama para AAC. Sensibilidad afecta la rama visual, no el sonido. colorkey elimina el negro del filtro antes de superponerlo, evitando un rectángulo opaco. FFprobe comprueba codec, resolución, fps y duración al finalizar.

## Polling, archivos y secretos

React consulta estado cada 1,5 segundos; eso es polling. El progreso deriva del tiempo FFmpeg procesado, no de una animación. IA no informa porcentaje y se muestra como fase indeterminada. Los resultados usan descarga HTTP navegable con cookie y Range; un Blob de un episodio grande duplicaría presión de memoria.

Variables de entorno configuran ejecutables, límites y proveedor. `.env` no se versiona. Cualquier variable empotrada en frontend puede ser leída por el usuario: la clave se usa solo en backend. Token de un trabajo tampoco es una clave OpenAI.

## Pruebas y ejercicios

`tests/test_subtitles.py` prueba casos límite sin FFmpeg. `test_render.py` genera audio sintético, exporta, decodifica cuadros y compara cambios por región. Un mock de proveedor prueba contratos sin pagar, pero no demuestra que las credenciales funcionen.

1. Agrega un preset visual coral. Solución orientativa: cambia Design desde un botón UI, conserva validación y exige guardar; verifica prueba antes/después.
2. Agrega un test de cue que cruza el final de preview. Solución: Cue(20,30), inicio=5, duración=20 debe resultar Cue(15,20).
3. Explica por qué dos Uvicorn workers fallarían. Cada proceso tendría registro/cola distintos y podría recibir una consulta sin conocer ese trabajo; file lock lo impide.
4. Añade un proveedor de pruebas que falle por timeout. Solución: inyéctalo en store.provider con monkeypatch, comprueba failed y que entradas siguen disponibles; jamás uses clave real en tests.
