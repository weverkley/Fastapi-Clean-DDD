from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables and .env file.
    
    Pydantic automatically reads and validates these settings.
    """
    
    # Use str for database URLs with custom schemes, as AnyUrl does not support non-standard schemes.
    APP_ENV: str = "development"
    SECRET_KEY: str = "qazwsxedc132"
    DATABASE_URL: str = "postgresql+asyncpg://root:12345678@localhost:5432/smgeo_consulta"

    # Configure the settings model to read from a .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

# Create a single, importable instance of the settings
settings = Settings()