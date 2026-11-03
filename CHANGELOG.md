# Cambios

## 0.2.0 · 2026-11-02

- Generación de SRT desde audio con Whisper local Tiny/Base, sin API de pago.
- Revisión, corrección, descarga, aprobación y reintento de transcripción.
- Resaltado opcional de palabra actual con amarillo configurable y tiempos estimados.
- Procesamiento por ventanas, supervisión/cancelación y limpieza de intermedios.
- 44 pruebas backend, 7 frontend y 2 Node; transcripción y MP4 reales con voz sintética.


## 0.1.0 · 2026-11-02

- Primera base web local: carga, diseño, prueba y exportación MP4.
- FastAPI con validación, cola, cancelación, TTL, tokens y descargas por streaming.
- FFmpeg nativo, subtítulos ASS y visualizadores onda/barras.
- Fondo local/propio y proveedor OpenAI opcional sin llamadas pagadas en pruebas.
- Documentación Windows/macOS, guía didáctica y pruebas sintéticas.

Consultar IMPLEMENTATION_STATUS para evidencia y pendientes; este registro no certifica pruebas en ambos OS.

## 0.3.0 · 2026-11-02

- Fuentes y tamaños independientes para título/subtítulos.
- Tres familias DejaVu incluidas y vista de composición con fuentes locales.
- Seis posiciones de logo y margen configurable; logo visible en composición.
- 56 pruebas backend y 9 frontend; renders y recorrido de navegador verificados.

## 0.4.0 · Fuentes amigables y negrilla (2026-11-03)

Diseño → Tipografía y logo incorpora Negrilla en el título y fuentes Nunito, Fredoka, Rounded y Poppins. Regular/Bold locales; JSON conserva title_bold (true por defecto). 69 pruebas backend y 10 frontend pasaron; pruebas multimedia de las cuatro familias en ambos pesos. Ver docs/DESIGN_CONTROLS.md y THIRD_PARTY_NOTICES.md para detalles/licencias.

## Licencia · 2026-11-03

- El propietario eligió MIT para el código propio de EasyPodcast.
- Se añadió LICENSE y se actualizaron documentación y metadatos de paquetes/lockfiles.
- Se mantienen las licencias de fuentes, modelos y dependencias de terceros.

## Conservación de episodios · 0.4.1 (2026-11-03)

Se amplía TTL_SECONDS de 3600 a 86400: 24 h tras creación o última operación completada. Fallos/cancelaciones siguen a 15 min y operaciones activas a 4 h. /api/capabilities expone retention. El polling renueva solo la cookie de medios hasta el vencimiento real; no prolonga el trabajo. Se mantienen borrado manual, limpieza y espera por descargas activas.

404/410 explican que el episodio pudo vencer, eliminarse, perderse en un reinicio o tener sesión inválida. La interfaz bloquea el render al detectar pérdida del trabajo, permite guardar el diseño aún en memoria como JSON y ofrece cargar otro episodio. Un clip visible puede estar en caché; no demuestra que el servidor conserve el audio. No hay persistencia entre reinicios: un trabajo ya eliminado no se restaura cambiando el límite.
