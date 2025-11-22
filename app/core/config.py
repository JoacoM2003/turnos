from pydantic_settings import BaseSettings
from pydantic import Field
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    secret_key: str = Field("change_me", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    api_v1: str = "/api/v1"
    project_name: str = "Turnero"

    backend_cors_origins: list[str] = [
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", "")
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
