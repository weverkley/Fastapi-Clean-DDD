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
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_EXCHANGE: str = "app.events"
    RABBITMQ_DLX_EXCHANGE: str = "app.events.dlx"
    USER_CREATED_QUEUE: str = "user.created.queue"
    USER_CREATED_ROUTING_KEY: str = "user.created.v1"
    USER_CREATED_DLQ: str = "user.created.dlq"
    USER_CREATED_DLQ_ROUTING_KEY: str = "user.created.dlq.v1"
    OUTBOX_BATCH_SIZE: int = 100
    OUTBOX_PUBLISH_INTERVAL_SECONDS: int = 2
    OUTBOX_MAX_ATTEMPTS: int = 10
    MESSAGE_BUS_PROVIDER: str = "rabbitmq"  # rabbitmq | gcp_pubsub
    GCP_PROJECT_ID: str = ""
    GCP_PUBSUB_DEFAULT_TOPIC: str = "app.events"
    GCP_PUBSUB_USER_CREATED_SUBSCRIPTION: str = "user-created-sub"

    # Configure the settings model to read from a .env file
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"
    )

# Create a single, importable instance of the settings
settings = Settings()
