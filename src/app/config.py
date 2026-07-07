from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "app"
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    database_url: str = "postgresql+psycopg://user:pass@localhost:5432/app"
    redis_url: str = "redis://localhost:6379/0"

    kafka_bootstrap_servers: str | None = None

    s3_endpoint_url: str | None = None
    s3_access_key: str | None = None
    s3_secret_key: str | None = None

    log_level: str = "INFO"
    log_format: str = "json"

    otel_traces_exporter: str = "console"
    otel_metrics_exporter: str = "console"

settings = Settings()
