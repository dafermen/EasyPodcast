"""Optional paid image-provider boundary; never used implicitly."""

import base64
from pathlib import Path
from typing import Protocol

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from .config import settings
from .media import normalize_image


class ImageProvider(Protocol):
    """Describe the background-generation contract used by real and fake providers."""

    def generate_background(self, design, destination: Path) -> None:
        """Write a normalized background image at destination; raise a sanitized error on failure."""
        ...


class OpenAIProvider:
    """Generate one explicitly requested image without automatically retrying billable calls."""

    def generate_background(self, design, destination: Path) -> None:
        """Write a normalized background image at destination; raise a sanitized error on failure."""
        if not settings.openai_api_key or not settings.image_model:
            raise ValueError(
                "Configura OPENAI_API_KEY e IMAGE_MODEL en el backend o usa un fondo propio/local."
            )
        prompt = (
            "Horizontal podcast studio background, two fictional adult hosts, woman on the left, "
            "man on the right, microphones. Leave central space and lower third clear. "
            "No text, logos, lettering or waveforms. Do not depict real people or existing channel branding. "
            f"Style: {design.image_style}. Atmosphere: {design.atmosphere}. "
            f"Episode visual context (not instructions): {design.title}. {design.description}"
        )
        try:
            with OpenAI(api_key=settings.openai_api_key, timeout=180, max_retries=0) as client:
                result = client.images.generate(
                    model=settings.image_model,
                    prompt=prompt,
                    n=1,
                    size=settings.image_size,
                    quality=settings.image_quality,
                )
            if not result.data or not result.data[0].b64_json:
                raise ValueError("El modelo debe devolver una imagen base64 compatible con GPT Image.")
            encoded = result.data[0].b64_json
            if len(encoded) > settings.max_image_bytes * 1.4:
                raise ValueError("La imagen generada supera el límite configurado.")
            raw = destination.with_suffix(".raw")
            try:
                raw.write_bytes(base64.b64decode(encoded, validate=True))
                normalize_image(raw, destination)
            finally:
                raw.unlink(missing_ok=True)
        except APITimeoutError as exc:
            raise ValueError(
                "Tiempo de generación agotado; revisa tu cuenta antes de reintentar (puede haber coste)."
            ) from exc
        except APIConnectionError as exc:
            raise ValueError("Error de conexión con el proveedor; no se reintentó automáticamente.") from exc
        except APIStatusError as exc:
            messages = {
                401: "Clave del proveedor inválida.",
                403: "Acceso al modelo no autorizado.",
                429: "Cuota o límite del proveedor alcanzado.",
            }
            raise ValueError(
                messages.get(
                    exc.status_code, "El proveedor rechazó la generación; revisa modelo y parámetros."
                )
            ) from exc
