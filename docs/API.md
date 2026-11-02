# API implementada

Base `/api`. OpenAPI interactivo `/docs`, esquema `/openapi.json`. Mutaciones exigen cabecera `Origin: http://127.0.0.1:8000` (o uno de los orígenes configurados). Todas las operaciones sobre un trabajo requieren `X-Job-Token`; solo artefactos admiten la cookie HttpOnly por trabajo. No hay listado público de trabajos. Tokens nunca en URL.

| Método y ruta | Contrato |
|---|---|
| GET /health | status/version sin secretos |
| GET /capabilities | FFmpeg/FFprobe/filtros/encoders/fuente, proveedor disponible y límites |
| POST /jobs | multipart audio; srt obligatorio con subtitle_mode=upload (default), ausente con subtitle_mode=generate; image/logo opcionales; query language=en/auto/es/pt/fr/de/it, model=tiny/base; 201 con id, token y Job |
| GET /jobs/{id} | estado, fase, progreso 0..1 o null, error seguro, metadata, warnings, config, aprobaciones, artefactos y expires_at UTC |
| PATCH /jobs/{id}/config | Design completo, campos omitidos reciben defaults; no es merge parcial |
| POST /jobs/{id}/background | encola generación explícita; conserva fondo anterior si falla |
| POST /jobs/{id}/background/approve | aprueba imagen actual |
| POST /jobs/{id}/preview | JSON `{"start":0}`; hasta 20 segundos o tiempo restante |
| POST /jobs/{id}/preview/approve | registra revisión de prueba actual |
| POST /jobs/{id}/render | exige fondo y prueba aprobados; encola exportación |
| POST /jobs/{id}/cancel | solicita cancelación idempotente |
| GET /jobs/{id}/artifacts/{kind} | background, preview, video, config; `download=true` fuerza descarga de medios; Range soportado |
| DELETE /jobs/{id} | solicita cancelación y borrado diferido si hay lectores; deleted=true |
| POST /jobs/{id}/transcribe | reintenta transcripción de un trabajo creado con modo generate |
| GET /jobs/{id}/subtitles | SRT revisable y disponibilidad de tiempos por palabra; exige header token |
| PUT /jobs/{id}/subtitles | JSON con srt; valida, invalida renders y elimina tiempos por palabra si cambia |
| POST /jobs/{id}/subtitles/approve | habilita continuar tras revisión |

Estados: ready, queued, transcribing, generating_image, rendering_preview, rendering_video, cancelling, cancelled, completed, failed. Job incluye subtitle_source, subtitles_ready, subtitles_approved y word_timestamps. Artefacto adicional subtitles descarga SRT original/generado/editado identificado por contexto. Design incorpora highlight_words y highlight_color (amarillo #FFD54A). Eliminados/expirados desaparecen del registro; no hay estado persistente expired.

Errores: 400 Host inválido; 403 Origin; 404 inexistente/token incorrecto/artefacto ausente; 408 carga incompleta agotada; 409 operación activa, falta aprobación/dependencias; 410 vencido antes de limpieza; 413 tamaño; 422 validación; 429 carga simultánea/límite de trabajos; 507 espacio. Cola llena devuelve 422 con explicación. El esquema multipart se declara explícitamente en OpenAPI; el receptor trabaja con streaming sin UploadFile ni spooling completo.

Ejemplo Python desde cliente local (token guardado solo en RAM):

```python
import httpx
with httpx.Client(base_url="http://127.0.0.1:8000", headers={"Origin":"http://127.0.0.1:8000"}) as c:
    with open("episode.wav","rb") as audio, open("episode.srt","rb") as srt:
        job=c.post("/api/jobs",files={"audio":audio,"srt":srt}).raise_for_status().json()
    headers={"X-Job-Token":job["token"]}
    status=c.get(f'/api/jobs/{job["id"]}',headers=headers).json()
```

Design y PreviewRequest exactos en OpenAPI y `app/models.py`; rechazan campos extra, NaN, colores arbitrarios y presets no permitidos. Config JSON no contiene claves, archivos, rutas ni tokens; importarlo no recupera medios ni garantiza repetir una imagen IA.

## Tipografía y logo (0.3.0)

Diseño → Tipografía y logo permite fuente y tamaño de título/subtítulos independientes, tres fuentes incluidas y seis posiciones de logo con margen. Guarda cambios y genera otra prueba antes de exportar. Design añade title_font, subtitle_font, title_font_size, logo_position y logo_margin. Fuentes por /api/fonts/{key}; logo autenticado por artifacts/logo. Detalles y verificaciones en docs/DESIGN_CONTROLS.md.
