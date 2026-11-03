# Guía de uso

1. Arranca EasyPodcast y abre el navegador. Revisa “Motor audiovisual listo”. Si faltan dependencias, ejecuta el doctor antes de exportar.
2. En Archivos selecciona audio y SRT. Opcionalmente añade fondo PNG/JPEG y logo PNG. Pulsa Crear episodio. Se verifica contenido real; la extensión no basta.
3. Al comenzar Diseño elige Configurar manualmente o Importar un diseño JSON descargado de EasyPodcast. El JSON incluye ajustes; carga audio, subtítulos, fondo y logo aparte. Revisa o modifica el diseño y pulsa Guardar diseño. La confirmación indica el siguiente paso: pulsa el botón verde Aprobar fondo y continuar. El fondo local está identificado como sin IA; no tiene presentadores. Una imagen propia permite conservar exactamente los mismos personajes en otros episodios.
4. Si configuraste OpenAI, “Generar imagen con IA” hace una llamada explícita con datos visuales. Revisa el resultado. Regenerar puede generar otro coste. Aprueba el fondo que quieres conservar.
5. Ajusta la prueba desde un segundo específico. Su duración es hasta 20 segundos, limitada al audio restante. Los subtítulos se recortan y desplazan para ese segmento. Reproduce el MP4: tiene prioridad sobre la aproximación CSS.
6. Aprueba la prueba y renderiza el episodio completo. El porcentaje procede del tiempo procesado por FFmpeg; durante IA no hay porcentaje. Puedes cancelar y reintentar.
7. Descarga MP4, fondo y JSON. El fondo es estático; el visualizador responde al audio. No hay movimiento labial. Para reutilizar personajes, vuelve a cargar el PNG descargado, no esperes repetirlos con el mismo prompt.

Un cambio de diseño elimina artefactos anteriores y exige una prueba nueva. El recorte de SRT posterior al final del audio requiere autorización explícita en Diseño. Los solapamientos y textos densos se avisan; no hay corrección de sincronización, traducción ni transcripción automática.

Archivos temporales vencen según la hora mostrada. Polling no extiende TTL. Eliminar borra al terminar la cancelación y las descargas activas. Reiniciar backend o recargar pestaña pierde la sesión; conserva tus originales. No hay historial ni reanudación.

Los subtítulos se ajustan por ancho con la fuente incluida; por defecto se admiten dos líneas y puedes elegir tres. Si un texto no cabe, se rechaza el render con instrucciones para corregirlo, sin truncarlo. Llaves se escapan y tras barras originales se añade un carácter invisible para impedir comandos ASS conservando los glifos visibles. Revisa siempre la prueba.

## Alternativa: subir solo audio

En Archivos selecciona Generar desde el audio (local), idioma y Tiny/Base. Sube audio sin SRT. Espera la transcripción, revisa/descarga el SRT y pulsa Aprobar subtítulos y diseñar. En Diseño, Resaltar la palabra actual usa amarillo por defecto y permite otro color. Con SRT propio o editado se usan subtítulos normales. Revisa la prueba porque los tiempos por palabra son estimados. Ver TRANSCRIPTION.md.

## Tipografía y logo (0.3.0)

Diseño → Tipografía y logo permite fuente y tamaño de título/subtítulos independientes, tres fuentes incluidas y seis posiciones de logo con margen. Guarda cambios y genera otra prueba antes de exportar. Design añade title_font, subtitle_font, title_font_size, logo_position y logo_margin. Fuentes por /api/fonts/{key}; logo autenticado por artifacts/logo. Detalles y verificaciones en docs/DESIGN_CONTROLS.md.

## 0.4.0 · Fuentes amigables y negrilla (2026-11-03)

Diseño → Tipografía y logo incorpora Negrilla en el título y fuentes Nunito, Fredoka, Rounded y Poppins. Regular/Bold locales; JSON conserva title_bold (true por defecto). 69 pruebas backend y 10 frontend pasaron; pruebas multimedia de las cuatro familias en ambos pesos. Ver docs/DESIGN_CONTROLS.md y THIRD_PARTY_NOTICES.md para detalles/licencias.

## Conservación de episodios · 0.4.1 (2026-11-03)

Se amplía TTL_SECONDS de 3600 a 86400: 24 h tras creación o última operación completada. Fallos/cancelaciones siguen a 15 min y operaciones activas a 4 h. /api/capabilities expone retention. El polling renueva solo la cookie de medios hasta el vencimiento real; no prolonga el trabajo. Se mantienen borrado manual, limpieza y espera por descargas activas.

404/410 explican que el episodio pudo vencer, eliminarse, perderse en un reinicio o tener sesión inválida. La interfaz bloquea el render al detectar pérdida del trabajo, permite guardar el diseño aún en memoria como JSON y ofrece cargar otro episodio. Un clip visible puede estar en caché; no demuestra que el servidor conserve el audio. No hay persistencia entre reinicios: un trabajo ya eliminado no se restaura cambiando el límite.
