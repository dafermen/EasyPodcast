import tempfile
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env", extra="ignore")
    ffmpeg: str = "ffmpeg"
    ffprobe: str = "ffprobe"
    node: str = "node"
    transcription_cache: Path = Path.home() / ".cache" / "easypodcast" / "models"
    transcription_allow_download: bool = True
    openai_api_key: str = ""
    image_model: str = ""
    image_size: str = "1536x1024"
    image_quality: str = "medium"
    temp_root: Path = Path(tempfile.gettempdir()) / "easypodcast"
    max_audio_bytes: int = Field(1024**3, gt=0)
    max_srt_bytes: int = Field(5 * 1024**2, gt=0)
    max_image_bytes: int = Field(20 * 1024**2, gt=0)
    max_pixels: int = Field(25_000_000, gt=0)
    max_duration: float = Field(7200, gt=0)
    ttl_seconds: int = Field(3600, gt=0)
    failure_ttl_seconds: int = Field(900, gt=0)
    active_ttl_seconds: int = Field(14400, gt=0)
    queue_size: int = Field(2, ge=1, le=8)
    max_jobs: int = Field(8, ge=1, le=100)
    min_free_bytes: int = Field(512 * 1024**2, ge=0)
    allowed_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ]


settings = Settings()
