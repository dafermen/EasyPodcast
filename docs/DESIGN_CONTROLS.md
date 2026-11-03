# Tipografía y posición del logo

Antes de generar la prueba o exportar, abre **Diseño → Tipografía y logo**.

- Fuente del título y fuente de subtítulos independientes: DejaVu Sans, DejaVu Serif y DejaVu Sans Mono. Se incluyen con licencia; no requieren fuentes instaladas en el sistema ni servicios externos.
- Tamaño del título: 28–110 px. Tamaño de subtítulos: 28–72 px. Los números corresponden a un video de 1920×1080, no a los píxeles de la ventana del navegador.
- Logo: arriba, centro o abajo, a izquierda o derecha; margen de 20–160 px. Los controles se habilitan si se cargó un logo PNG en Archivos.

La vista de composición carga las mismas fuentes del backend y muestra el logo. Es aproximada; **la prueba MP4 es la referencia final**. Evita tapar título, subtítulos o rostros con el logo. Si un título muy grande no cabe sobre la onda, se explica el problema para reducir tamaño o texto.

Pulsa **Guardar diseño** tras ajustar. Se invalidan pruebas y videos anteriores; genera una prueba nueva, revísala y apruébala antes de exportar. La configuración JSON conserva fuente, tamaños, posición y margen. Los JSON anteriores reciben valores predeterminados compatibles.

API: Design añade title_font, subtitle_font (sans/serif/mono), title_font_size, logo_position y logo_margin; font_size sigue siendo el tamaño de subtítulos. `/api/fonts/{key}` sirve únicamente las fuentes incluidas mediante una lista permitida. El logo del trabajo se consulta en `/api/jobs/{id}/artifacts/logo`, con la misma autenticación que el resto de medios. No se admiten nombres de fuentes, rutas o filtros arbitrarios del cliente.

Validación: 56 pruebas backend y 9 frontend pasaron en Windows. Incluye estilos ASS, límites, rutas de fuentes, acceso al logo y renders FFmpeg reales con Serif en título, Mono en subtítulos y logos arriba a la izquierda/abajo a la derecha, comprobados por píxeles. macOS nativo y preferencias visuales del usuario siguen pendientes de revisión.

## Fuentes amigables y negrilla (0.4.0)

Se añaden Nunito (redondeada), Fredoka (expresiva), Rounded (derivada de Quicksand) y Poppins (moderna). Están disponibles tanto para título como para subtítulos. La casilla Negrilla en el título selecciona archivos Regular/Bold de peso 400/700. El peso se comparte entre la vista del navegador, la medición del ajuste de líneas y ASS/FFmpeg. Los diseños JSON conservan title_bold; si se omite, sigue siendo true para mantener el título anterior. No se descargan fuentes durante el uso: todos los archivos y licencias están incluidos.
