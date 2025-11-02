"""
Configuration module for the Orunmila AI Agent.
Handles environment variables and application settings.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application Settings
    app_name: str = Field(default="Orunmila - Yoruba History & Culture AI Agent")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", description="OpenAI API key for the AI agent")
    
    # Telex.im Configuration
    telex_api_key: str = Field(default="", description="Telex.im API key")
    telex_webhook_secret: str = Field(default="", description="Webhook secret for validating Telex.im requests")
    telex_bot_id: str = Field(default="", description="Bot ID on Telex.im platform")
    telex_api_url: str = Field(default="https://api.telex.im/v1", description="Telex.im API base URL")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_enabled: bool = Field(default=False)
    
    # CORS Settings
    cors_origins: List[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: List[str] = Field(default=["*"])
    cors_allow_headers: List[str] = Field(default=["*"])
    
    # Logging
    log_level: str = Field(default="INFO")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
