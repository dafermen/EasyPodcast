import base64
from types import SimpleNamespace

import httpx
import pytest
from app.config import settings
from app.images import OpenAIProvider
from openai import APIStatusError
from PIL import Image


def test_official_sdk_contract_without_network(monkeypatch, tmp_path):
    source = tmp_path / "source.png"
    Image.new("RGB", (100, 100), "navy").save(source)
    captured = {}

    class FakeClient:
        def __init__(self, **kwargs):
            captured["client"] = kwargs
            self.images = self

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def generate(self, **kwargs):
            captured["request"] = kwargs
            return SimpleNamespace(
                data=[SimpleNamespace(b64_json=base64.b64encode(source.read_bytes()).decode())]
            )

    monkeypatch.setattr("app.images.OpenAI", FakeClient)
    monkeypatch.setattr(settings, "openai_api_key", "fake-only")
    monkeypatch.setattr(settings, "image_model", "contract-model")
    from app.models import Design

    target = tmp_path / "background.png"
    OpenAIProvider().generate_background(Design(), target)
    assert Image.open(target).size == (1920, 1080)
    assert captured["client"]["max_retries"] == 0
    assert captured["request"]["size"] == "1536x1024"
    assert captured["request"]["model"] == "contract-model"
    assert "srt" not in captured["request"] and "audio" not in captured["request"]


@pytest.mark.parametrize("code", [401, 403, 429, 500])
def test_sdk_errors_do_not_leak_response(monkeypatch, tmp_path, code):
    class FakeClient:
        def __init__(self, **kwargs):
            self.images = self

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def generate(self, **kwargs):
            response = httpx.Response(
                code, request=httpx.Request("POST", "https://api.openai.com/v1/images/generations")
            )
            raise APIStatusError("secret-details", response=response, body=None)

    monkeypatch.setattr("app.images.OpenAI", FakeClient)
    monkeypatch.setattr(settings, "openai_api_key", "fake-only")
    monkeypatch.setattr(settings, "image_model", "contract-model")
    from app.models import Design

    with pytest.raises(ValueError) as error:
        OpenAIProvider().generate_background(Design(), tmp_path / "background.png")
    assert "secret-details" not in str(error.value)
