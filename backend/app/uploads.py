"""Bound each multipart file as bytes arrive, before any full-file spooling."""

import shutil

from fastapi import HTTPException
from python_multipart.exceptions import MultipartParseError
from python_multipart.multipart import MultipartParser, parse_options_header

from .config import settings


async def receive_files(request, directory):
    media_type, options = parse_options_header(request.headers.get("content-type", ""))
    boundary = options.get(b"boundary")
    if media_type != b"multipart/form-data" or not boundary or len(boundary) > 200:
        raise HTTPException(422, "Se requiere multipart/form-data con un boundary válido.")
    limits = {
        "audio": settings.max_audio_bytes,
        "srt": settings.max_srt_bytes,
        "image": settings.max_image_bytes,
        "logo": settings.max_image_bytes,
    }
    names = {"audio": "audio.bin", "srt": "original.srt", "image": "image.bin", "logo": "logo.bin"}
    seen = set()
    current = {
        "file": None,
        "name": None,
        "size": 0,
        "headers": {},
        "field": b"",
        "value": b"",
        "header_bytes": 0,
        "ended": False,
    }

    def part_begin():
        current.update(file=None, name=None, size=0, headers={}, field=b"", value=b"", header_bytes=0)

    def header_field(data, start, end):
        current["header_bytes"] += end - start
        if current["header_bytes"] > 8192:
            raise HTTPException(413, "Cabeceras multipart demasiado grandes.")
        current["field"] += data[start:end]

    def header_value(data, start, end):
        current["header_bytes"] += end - start
        if current["header_bytes"] > 8192:
            raise HTTPException(413, "Cabeceras multipart demasiado grandes.")
        current["value"] += data[start:end]

    def header_end():
        current["headers"][current["field"].lower()] = current["value"]
        current["field"], current["value"] = b"", b""

    def headers_finished():
        _, opts = parse_options_header(current["headers"].get(b"content-disposition", b""))
        name = opts.get(b"name", b"").decode("utf-8", errors="replace")
        if name not in names or name in seen or b"filename" not in opts:
            raise HTTPException(422, "Archivo desconocido, duplicado o campo sin archivo.")
        seen.add(name)
        current["name"] = name
        current["file"] = (directory / names[name]).open("wb")

    def part_data(data, start, end):
        current["size"] += end - start
        if current["size"] > limits[current["name"]]:
            raise HTTPException(413, f"El archivo {current['name']} supera su límite.")
        if shutil.disk_usage(directory).free < settings.min_free_bytes + end - start:
            raise HTTPException(507, "Espacio libre insuficiente durante la carga.")
        current["file"].write(data[start:end])

    def part_end():
        current["file"].close()
        current["file"] = None
        if not current["size"]:
            raise HTTPException(422, "No se admiten archivos vacíos.")

    def finished():
        current["ended"] = True

    parser = MultipartParser(
        boundary,
        {
            "on_part_begin": part_begin,
            "on_header_field": header_field,
            "on_header_value": header_value,
            "on_header_end": header_end,
            "on_headers_finished": headers_finished,
            "on_part_data": part_data,
            "on_part_end": part_end,
            "on_end": finished,
        },
    )
    try:
        async for chunk in request.stream():
            parser.write(chunk)
        parser.finalize()
        if not current["ended"] or not {"audio", "srt"}.issubset(seen):
            raise HTTPException(422, "Carga incompleta: se necesitan audio y SRT.")
        return seen
    except MultipartParseError as exc:
        raise HTTPException(422, "Carga multipart inválida.") from exc
    finally:
        if current["file"]:
            current["file"].close()
