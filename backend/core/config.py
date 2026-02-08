from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    BETTER_AUTH_SECRET: str
    COHERE_API_KEY: str
    ENVIRONMENT: str = "development"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Write this line directly inside the class (instead of Config class)
    model_config = SettingsConfigDict(
        env_file=".env",              # Load .env file
        env_ignore_empty=True,        # Ignore empty values
        extra='allow'                 # Allow extra fields (api_base_url etc.)
    )

settings = Settings()