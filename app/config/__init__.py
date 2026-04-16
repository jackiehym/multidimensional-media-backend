from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env"
    )
    DATABASE_URL: str = "sqlite:///./media.db"
    MEDIA_DIR: str = "./media"
    UPLOAD_DIR: str = "./uploads"
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    ENVIRONMENT: str = "development"


settings = Settings()