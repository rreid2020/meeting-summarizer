# app/config.py
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"  # Default SQLite for testing
    stripe_secret_key: str = "test_key"
    stripe_webhook_secret: str = "test_webhook"
    zoom_client_id: str = "test_zoom_id"
    zoom_client_secret: str = "test_zoom_secret"
    teams_client_id: str = "test_teams_id"
    teams_client_secret: str = "test_teams_secret"
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "test_openai_key")
    
    class Config:
        env_file = ".env"