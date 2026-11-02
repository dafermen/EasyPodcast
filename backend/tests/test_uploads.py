from types import SimpleNamespace

import pytest
from app.config import settings
from app.uploads import receive_files
from fastapi import HTTPException


def test_chunked_file_limit_aborts_before_receiving_rest(tmp_path, monkeypatch):
    import asyncio

    monkeypatch.setattr(settings, "max_audio_bytes", 10)
    monkeypatch.setattr(settings, "min_free_bytes", 0)
    consumed = []

    async def stream():
        yield b'--boundary\r\nContent-Disposition: form-data; name="audio"; filename="../../x.wav"\r\n\r\n'
        for i in range(100):
            consumed.append(i)
            yield b"12345678"
        yield b"\r\n--boundary--\r\n"

    request = SimpleNamespace(
        headers={"content-type": "multipart/form-data; boundary=boundary"}, stream=stream
    )
    with pytest.raises(HTTPException) as error:
        asyncio.run(receive_files(request, tmp_path))
    assert error.value.status_code == 413
    assert len(consumed) < 5
    assert (tmp_path / "audio.bin").stat().st_size <= 10


def test_missing_boundary_is_rejected(tmp_path):
    import asyncio

    request = SimpleNamespace(headers={"content-type": "text/plain"})
    with pytest.raises(HTTPException) as error:
        asyncio.run(receive_files(request, tmp_path))
    assert error.value.status_code == 422
