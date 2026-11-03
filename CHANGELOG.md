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
