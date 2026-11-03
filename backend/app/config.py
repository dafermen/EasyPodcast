"""Backend settings and their validated defaults."""

import tempfile
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Read bounded backend configuration from environment variables and the repository .env file."""

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env", extra="ignore")
    # FFMPEG: see docs/CONFIGURATION.md for units, defaults and operational effects.
    library_root: Path = Path.home() / ".easypodcast" / "library"
    ffmpeg: str = "ffmpeg"
    # FFPROBE: see docs/CONFIGURATION.md for units, defaults and operational effects.
    ffprobe: str = "ffprobe"
    # NODE: see docs/CONFIGURATION.md for units, defaults and operational effects.
    node: str = "node"
    # TRANSCRIPTION_CACHE: see docs/CONFIGURATION.md for units, defaults and operational effects.
    transcription_cache: Path = Path.home() / ".cache" / "easypodcast" / "models"
    # TRANSCRIPTION_ALLOW_DOWNLOAD: see docs/CONFIGURATION.md for units, defaults and operational effects.
    transcription_allow_download: bool = True
    # OPENAI_API_KEY: see docs/CONFIGURATION.md for units, defaults and operational effects.
    openai_api_key: str = ""
    # IMAGE_MODEL: see docs/CONFIGURATION.md for units, defaults and operational effects.
    image_model: str = ""
    # IMAGE_SIZE: see docs/CONFIGURATION.md for units, defaults and operational effects.
    image_size: str = "1536x1024"
    # IMAGE_QUALITY: see docs/CONFIGURATION.md for units, defaults and operational effects.
    image_quality: str = "medium"
    # TEMP_ROOT: see docs/CONFIGURATION.md for units, defaults and operational effects.
    temp_root: Path = Path(tempfile.gettempdir()) / "easypodcast"
    # MAX_AUDIO_BYTES: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_audio_bytes: int = Field(1024**3, gt=0)
    # MAX_SRT_BYTES: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_srt_bytes: int = Field(5 * 1024**2, gt=0)
    # MAX_IMAGE_BYTES: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_image_bytes: int = Field(20 * 1024**2, gt=0)
    # MAX_PIXELS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_pixels: int = Field(25_000_000, gt=0)
    # MAX_DURATION: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_duration: float = Field(7200, gt=0)
    # TTL_SECONDS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    ttl_seconds: int = Field(86400, gt=0)
    # FAILURE_TTL_SECONDS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    failure_ttl_seconds: int = Field(900, gt=0)
    # ACTIVE_TTL_SECONDS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    active_ttl_seconds: int = Field(14400, gt=0)
    # QUEUE_SIZE: see docs/CONFIGURATION.md for units, defaults and operational effects.
    queue_size: int = Field(2, ge=1, le=8)
    # MAX_JOBS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    max_jobs: int = Field(8, ge=1, le=100)
    # MIN_FREE_BYTES: see docs/CONFIGURATION.md for units, defaults and operational effects.
    min_free_bytes: int = Field(512 * 1024**2, ge=0)
    # ALLOWED_ORIGINS: see docs/CONFIGURATION.md for units, defaults and operational effects.
    allowed_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]


settings = Settings()
