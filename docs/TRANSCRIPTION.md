# Subtítulos automáticos y resaltado

En Archivos elige «Generar desde el audio (local)», idioma y modelo Tiny/Base. No se necesita un SRT ni una clave de API. También se conserva la opción «Ya tengo un archivo SRT».

## Instalación

Node 22.12+ y FFmpeg son necesarios. Desde la raíz ejecuta `npm --prefix transcription ci` (Windows: `npm.cmd --prefix transcription ci`). Reinicia backend y revisa `/api/capabilities`, campo `transcription.available`.

La primera generación descarga el modelo de Hugging Face; los audios no salen del equipo. Los archivos de modelo se guardan persistentemente en `~/.cache/easypodcast/models`, fuera del repositorio y de los temporales de episodios. Puedes cambiar TRANSCRIPTION_CACHE y desactivar nuevas descargas con TRANSCRIPTION_ALLOW_DOWNLOAD=false. Sin modelos en caché, ese modo fallará con un mensaje y permite usar SRT propio. No se hace ninguna llamada pagada.

## Flujo

1. Selecciona solo audio y, opcionalmente, fondo/logo.
2. Crea el episodio; entra en cola y luego transcribe. Tiny es más ligero; Base consume más tiempo/recursos. El idioma elegido es el del contenido, no una traducción.
3. Descarga el SRT o abre «Revisar o corregir SRT». Revisa reconocimiento y sincronización: pueden existir errores y alucinaciones, especialmente con música, ruido y silencios.
4. Aprueba los subtítulos para habilitar Diseño. Allí puedes desactivar «Resaltar la palabra actual» o cambiar el amarillo inicial.
5. Guarda diseño, aprueba fondo y genera una prueba. El resaltado está quemado en el video final mediante ASS/libass; no identifica hablantes.

Un SRT no guarda tiempos por palabra. Por eso el resaltado solo está disponible con la transcripción generada en esta sesión. **Guardar cambios de texto/tiempos al SRT elimina esos tiempos internos** para no señalar palabras equivocadas; los subtítulos normales siguen funcionando. Guardar sin cambios conserva los tiempos. Descargar/importar el SRT en otro trabajo tampoco recupera el resaltado. No se inventa alineación uniforme para SRT propios.

## Arquitectura y límites

Backend FastAPI conserva la cola, token, aprobación, cancelación y TTL. FFmpeg crea temporal PCM float32 mono 16 kHz (64 KB/s). El subproceso Node usa Transformers.js/Whisper CPU q8, lee ventanas de máximo 30 segundos con contexto de 5 s y núcleos únicos de 20 s. Solo las muestras de una ventana están en RAM. Las palabras se asignan al núcleo por el punto medio y los solapamientos entre palabras se ajustan al final anterior; estos tiempos son **estimados por el modelo**, no alineación forzada certificada. Los chunks sin inicio/final finitos se omiten; sin palabras válidas se informa fallo. Revisar bordes de ventanas en podcasts reales.

El progreso corresponde a segundos de núcleos procesados, no a una ETA; carga/descarga de modelo es indeterminada. PCM y JSON intermedios se borran en éxito, fallo y cancelación. Se supervisan timeout, disco y árbol de procesos. Modelos no se borran al vencer un episodio porque son caché reutilizable. El límite máximo de audio sigue siendo el de producto, no un benchmark de transcripción de dos horas.

Referencias: [Transformers.js ASR con tiempos por palabra](https://huggingface.co/docs/transformers.js/api/pipelines#module_pipelines.AutomaticSpeechRecognitionPipeline), modelos [Tiny](https://huggingface.co/Xenova/whisper-tiny) y [Base](https://huggingface.co/Xenova/whisper-base). Se tomó como referencia arquitectónica vDownloader, sin cambiar sus archivos ni depender de su servicio.

## Verificación

Pruebas Python de modo inicial, autenticación, revisión, descarga, edición, reintento, cancelación y recorte temporal del resaltado. Pruebas Node de silencio y selección de palabras en ventanas superpuestas (`npm --prefix transcription test`). Se ejecutó Whisper Tiny real, CPU q8, sobre voz inglesa sintética local de 4,435 s; reconoció 11 palabras con tiempos. La exactitud de voz humana y episodios largos requiere revisión adicional; el benchmark previo de render no mide transcripción.
