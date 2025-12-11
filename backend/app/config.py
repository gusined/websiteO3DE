import os
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Application"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A comprehensive FastAPI application"
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    REDIS_URL: str = "redis://localhost:6379"
    
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    class Config:
        env_file = ".env"

settings = Settings()