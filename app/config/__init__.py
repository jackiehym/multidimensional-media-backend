from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path
from typing import Optional


# 获取 backend 目录的绝对路径
BACKEND_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env"
    )
    DATABASE_URL: str = f"sqlite:///{BACKEND_DIR}/media.db"
    MEDIA_DIR: str = str(BACKEND_DIR / "media")
    UPLOAD_DIR: str = str(BACKEND_DIR / "uploads")
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"


settings = Settings()