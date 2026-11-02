# Producto

EasyPodcast convierte un audio y su SRT sincronizado en un video descargable para un creador hispanohablante. El contenido puede estar en cualquier idioma compatible con la fuente. NotebookLM queda fuera: el usuario aporta sus archivos.

## Alcance de esta versión

Web local multiplataforma: React/TypeScript/Vite y Python/FastAPI/FFmpeg. MP3, WAV, M4A; SRT UTF-8 con/sin BOM; fondo PNG/JPEG y logo PNG. Exportación H.264/AAC, 1920×1080, 30 fps, yuv420p, faststart. No altera velocidad/tono ni normaliza audio. Selecciona la primera pista si hay varias e informa de ello.

El usuario carga, diseña, aprueba el fondo, renderiza y revisa una prueba corta, aprueba esa prueba y exporta. Cada cambio de diseño invalida prueba/video. La imagen se conserva salvo regeneración explícita. El fondo local es decorativo, sin presentadores y sin IA; el proveedor opcional pide dos adultos ficticios con espacio central e inferior libre.

El visualizador responde a la mezcla de audio; no detecta hablantes ni mide decibelios calibrados. No hay animación labial. La vista CSS es orientativa; la prueba MP4 es la referencia.

## Aceptación

Un usuario debe producir un MP4 desde navegador sin consola una vez instalado. Los errores deben ser accionables. No se debe aceptar video parcial como artefacto válido. Deben conservarse entradas para reintento tras cancelar, proteger cada trabajo y borrar medios al vencer sin interrumpir lectores activos. Los límites no constituyen garantías de rendimiento.

## Exclusiones

Publicación YouTube, monetización garantizada, cuentas, colaboración remota, base de datos, historial, móviles nativos, transcripción, traducción, diarización, clonación de voz, lip sync, editor SRT completo y render distribuido. Xcode no forma parte del proyecto. El propietario decide licencia y futuras opciones de alojamiento.
