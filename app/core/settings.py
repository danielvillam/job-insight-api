"""Configuracion centralizada de la aplicacion."""

from pydantic import Field
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Define variables de entorno y sus valores por defecto."""

    app_name: str = "Job Insight API"
    app_version: str = "1.1.0"
    app_description: str = (
        "API para analizar descripciones de vacantes de empleo, "
        "compararlas con perfiles de desarrolladores y generar "
        "recomendaciones de aprendizaje."
    )
    debug: bool = False

    database_url: str = "sqlite+aiosqlite:///./job_insight.db"
    cors_allow_origins: list[str] = Field(default_factory=lambda: ["*"])
    cors_allow_credentials: bool = False

    rate_limit_analyze_job: str = "30/minute"
    rate_limit_match_profile: str = "30/minute"
    rate_limit_learning_path: str = "30/minute"
    rate_limit_full_report: str = "20/minute"
    rate_limit_trust_proxy_headers: bool = False

    request_max_description_length: int = 10000

    @model_validator(mode="after")
    def validate_cors(self) -> "Settings":
        if self.cors_allow_credentials and "*" in self.cors_allow_origins:
            raise ValueError(
                "Invalid CORS configuration: '*' cannot be used with credentials enabled."
            )
        return self

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
