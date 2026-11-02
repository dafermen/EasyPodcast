# Avisos de terceros

La licencia del código EasyPodcast queda pendiente de decisión de su propietario. No se crea una licencia supuesta.

## Fuente incluida

DejaVu Sans se incluye en `assets/fonts/DejaVuSans.ttf` con licencia íntegra en `assets/fonts/LICENSE-DejaVu.txt`. Fuente del binario: repositorio matplotlib, etiqueta v3.10.8, `lib/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf`; fuente de licencia: repositorio dejavu-fonts/dejavu-fonts. DejaVu conserva condiciones Bitstream Vera y avisos aplicables. No se modifica la fuente.

## FFmpeg

FFmpeg y FFprobe son dependencias externas; el repositorio no incluye sus binarios. Sus obligaciones dependen de la compilación: libx264 suele implicar GPL; revisar configuración y licencias antes de distribuir binarios o empaquetar instaladores. La compilación local inspeccionada anuncia GPL y version3. No asumir una licencia única para toda distribución FFmpeg. [Licencias oficiales](https://ffmpeg.org/legal.html).

## Paquetes

React, Vite, FastAPI, Pillow, Pydantic, OpenAI SDK y demás dependencias conservan sus licencias y avisos en los paquetes instalados. Locks registran versiones exactas; revisar avisos antes de redistribuir. EasyPodcast no incluye audio personal ni imágenes de terceros sin licencia. La revisión editorial y derechos del contenido corresponden al creador.

## Transcripción opcional

Transformers.js (@huggingface/transformers), Apache-2.0; ONNX Runtime y dependencias conservan sus licencias instaladas. Modelos Xenova/whisper-tiny y Xenova/whisper-base: las fichas oficiales declaran Apache-2.0. No se incluyen pesos en Git. Se descargan o reutilizan localmente en caché. Revisar sus fichas/licencias antes de redistribuir modelos: https://huggingface.co/Xenova/whisper-tiny y https://huggingface.co/Xenova/whisper-base .

Se incluyen además DejaVuSerif.ttf y DejaVuSansMono.ttf, sin modificar, del mismo origen matplotlib v3.10.8. Conservan la licencia DejaVu/Bitstream íntegra ya incluida en assets/fonts/LICENSE-DejaVu.txt.
