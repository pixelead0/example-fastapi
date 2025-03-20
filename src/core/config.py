import os
import logging
from typing import List, Optional, Union
from pydantic import validator, PostgresDsn
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application config
    APP_NAME: str = "Product Management API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    
    # Logging
    LOG_LEVEL: Union[int, str] = logging.INFO
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./productdb.db"
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Security
    SECRET_KEY: str = "secret-key-for-development-only"
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        if isinstance(v, str):
            try:
                return getattr(logging, v.upper())
            except AttributeError:
                return logging.INFO
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignora variables adicionales en el archivo .env


@lru_cache()
def get_settings() -> Settings:
    """Create settings once and cache them."""
    return Settings() 