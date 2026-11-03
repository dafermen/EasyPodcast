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

## Fuentes adicionales (2026-11-03)

Baloo 2, Outfit, Balsamiq Sans, Lexend, Atkinson Hyperlegible y Comic Neue proceden de https://github.com/google/fonts/tree/main/ofl (carpetas baloo2, outfit, balsamiqsans, lexend, atkinsonhyperlegible y comicneue). Licencias SIL OFL 1.1 completas en assets/fonts/LICENSE-{familia}.txt, con los avisos de autor originales. Baloo 2, Outfit y Lexend se instanciaron de las fuentes variables a pesos 400/700 con fontTools 4.68.0; nombres de estilo Regular/Bold. Las restantes son TTF estáticas originales sin modificar. No se usa el nombre reservado RevReading Lexend. Comic Neue no es Comic Sans MS. No se incluyen archivos de fuentes de Windows.

SHA-256 de archivos incorporados:

- `Baloo2-Regular.ttf`: `e199f911068787e1f44c20731a127c50e8ea89ef63a5f91d35d6c645d307de90`
- `Baloo2-Bold.ttf`: `34fb5cd63d531229a0b5597bbcc0365817c6bcb61bee19cc8a48e6de8f6dd6c1`
- `Outfit-Regular.ttf`: `a797f8520a9cdcfedd144db407ff2821dcd36e2fb849383848d3f642f1c985ad`
- `Outfit-Bold.ttf`: `d09058727a4113189d59a6ce9f8e1d375340fa90cc6f16f3d3611ebfadc2abf2`
- `BalsamiqSans-Regular.ttf`: `fcc9c00a9ad6e78673fa84653745569097241d99b5d1387a23f395858ed46b7e`
- `BalsamiqSans-Bold.ttf`: `a3302bd8424e6a37704eb5e20d5c5a3a2fd80feaf57e48a19d261f8e0c583621`
- `Lexend-Regular.ttf`: `f4dfaaa5c745eaff3526df098444358e015e58792b5063af8f0ee346cf038e01`
- `Lexend-Bold.ttf`: `6b4d8ea498442250e3d1b411b7a62c069375a88af0b12a8d25bfa2690afd729f`
- `AtkinsonHyperlegible-Regular.ttf`: `7fb917c89019896d0b52ee84b7cbb3304c18cb90b19a62f5e32712bd23e97669`
- `AtkinsonHyperlegible-Bold.ttf`: `5a3b0c8cc8ca545155150b4512a1fa248298df121c50d6557e651e61fbdab92f`
- `ComicNeue-Regular.ttf`: `a0ee5a37c8b27c4db0700137d928598b1e23b0089e1546a8961909176b779360`
- `ComicNeue-Bold.ttf`: `3e7e5fccfd7e0788f317b43312151c1bd5cf058c9697a8d83eac3939050bd61e`
