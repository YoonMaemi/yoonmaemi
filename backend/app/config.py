"""Application configuration helpers."""

from functools import lru_cache
import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]

for env_path in (PROJECT_ROOT / ".env", BACKEND_ROOT / ".env"):
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)


class Settings:
    """Container for runtime configuration values."""

    def __init__(
        self,
        *,
        gemini_api_key: Optional[str] = None,
        gemini_model: str = "gemini-2.0-flash",
    ) -> None:
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.gemini_model = gemini_model or os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    def validate(self) -> None:
        if not self.gemini_api_key:
            raise RuntimeError(
                "Missing Gemini API key. Set GEMINI_API_KEY in your .env file or environment."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
