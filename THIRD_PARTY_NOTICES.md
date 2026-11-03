# Avisos de terceros

El código propio de EasyPodcast se distribuye bajo la licencia MIT, elegida por su propietario el 3 de noviembre de 2026. Consulta LICENSE. Esta elección no modifica las licencias ni los avisos de fuentes, modelos y dependencias de terceros.

## Fuente incluida

DejaVu Sans se incluye en `assets/fonts/DejaVuSans.ttf` con licencia íntegra en `assets/fonts/LICENSE-DejaVu.txt`. Fuente del binario: repositorio matplotlib, etiqueta v3.10.8, `lib/matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf`; fuente de licencia: repositorio dejavu-fonts/dejavu-fonts. DejaVu conserva condiciones Bitstream Vera y avisos aplicables. No se modifica la fuente.

## FFmpeg

FFmpeg y FFprobe son dependencias externas; el repositorio no incluye sus binarios. Sus obligaciones dependen de la compilación: libx264 suele implicar GPL; revisar configuración y licencias antes de distribuir binarios o empaquetar instaladores. La compilación local inspeccionada anuncia GPL y version3. No asumir una licencia única para toda distribución FFmpeg. [Licencias oficiales](https://ffmpeg.org/legal.html).

## Paquetes

React, Vite, FastAPI, Pillow, Pydantic, OpenAI SDK y demás dependencias conservan sus licencias y avisos en los paquetes instalados. Locks registran versiones exactas; revisar avisos antes de redistribuir. EasyPodcast no incluye audio personal ni imágenes de terceros sin licencia. La revisión editorial y derechos del contenido corresponden al creador.

## Transcripción opcional

Transformers.js (@huggingface/transformers), Apache-2.0; ONNX Runtime y dependencias conservan sus licencias instaladas. Modelos Xenova/whisper-tiny y Xenova/whisper-base: las fichas oficiales declaran Apache-2.0. No se incluyen pesos en Git. Se descargan o reutilizan localmente en caché. Revisar sus fichas/licencias antes de redistribuir modelos: https://huggingface.co/Xenova/whisper-tiny y https://huggingface.co/Xenova/whisper-base .

Se incluyen además DejaVuSerif.ttf y DejaVuSansMono.ttf, sin modificar, del mismo origen matplotlib v3.10.8. Conservan la licencia DejaVu/Bitstream íntegra ya incluida en assets/fonts/LICENSE-DejaVu.txt.

## Fuentes amigables · 0.4.0

Nunito, Fredoka y Poppins se incluyen con sus licencias SIL OFL 1.1 en assets/fonts/LICENSE-nunito.txt, LICENSE-fredoka.txt y LICENSE-poppins.txt. Origen: repositorio oficial google/fonts, directorios ofl/nunito, ofl/fredoka, ofl/poppins. Nunito/Fredoka se instanciaron a pesos estáticos 400/700 con FontTools 4.68.0; Fredoka usa anchura normal. Poppins son archivos estáticos oficiales sin modificar.

EasyPodcast Rounded es una derivación estática 400/700 de Quicksand (google/fonts/ofl/quicksand), renombrada porque Quicksand es un Reserved Font Name. Se conservan derechos y licencia íntegra en LICENSE-quicksand.txt. No se vende la fuente por separado. FontTools es una herramienta de preparación, no una dependencia para usar la aplicación. Se añaden también variantes Bold oficiales DejaVu del mismo origen matplotlib v3.10.8 y licencia ya incluida.
