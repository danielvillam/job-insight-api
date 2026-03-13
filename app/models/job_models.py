"""Modelos Pydantic para análisis de vacantes."""

from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    """Cuerpo de la petición para analizar una oferta laboral."""

    description: str = Field(
        ...,
        min_length=20,
        examples=[
            "We are looking for a Python developer with 3+ years of experience "
            "in Django and REST APIs. Knowledge of Docker and PostgreSQL is a plus."
        ],
        description="Texto completo de la descripción de la vacante.",
    )

    model_config = {"json_schema_extra": {"examples": [{"description": (
        "We are looking for a Python developer with 3+ years of experience "
        "in Django and REST APIs. Knowledge of Docker and PostgreSQL is a plus."
    )}]}}


class ExtractedSkills(BaseModel):
    """Resultado del análisis de habilidades de una vacante."""

    tech_skills: list[str] = Field(
        default_factory=list,
        description="Habilidades técnicas detectadas en la vacante.",
    )
    soft_skills: list[str] = Field(
        default_factory=list,
        description="Habilidades blandas detectadas en la vacante.",
    )
    experience_years: int | None = Field(
        default=None,
        description="Años de experiencia requeridos (si se menciona).",
    )


class JobAnalysisResponse(BaseModel):
    """Respuesta del endpoint /analyze-job."""

    tech_skills: list[str]
    soft_skills: list[str]
    experience_years: int | None = None
    total_skills_found: int
