"""Modelos Pydantic para perfiles y comparación."""

from pydantic import BaseModel, Field


class MatchProfileRequest(BaseModel):
    """Cuerpo de la petición para comparar perfil con vacante."""

    profile_skills: list[str] = Field(
        ...,
        min_length=1,
        examples=[["python", "django", "docker", "postgresql"]],
        description="Lista de habilidades del perfil del desarrollador.",
    )
    job_description: str = Field(
        ...,
        min_length=20,
        description="Texto completo de la descripción de la vacante.",
    )


class MatchProfileResponse(BaseModel):
    """Respuesta del endpoint /match-profile."""

    compatibility_percentage: float = Field(
        ..., ge=0, le=100,
        description="Porcentaje de compatibilidad entre perfil y vacante.",
    )
    matching_skills: list[str]
    missing_skills: list[str]
    total_job_skills: int


class LearningPathRequest(BaseModel):
    """Cuerpo de la petición para generar ruta de aprendizaje."""

    missing_skills: list[str] = Field(
        ...,
        min_length=1,
        examples=[["docker", "kubernetes", "aws"]],
        description="Lista de habilidades faltantes.",
    )


class LearningRecommendation(BaseModel):
    """Recomendación individual de aprendizaje."""

    skill: str
    category: str | None
    priority: str = Field(description="high, medium o low")
    suggestion: str = Field(description="Sugerencia de recurso o ruta de estudio.")


class LearningPathResponse(BaseModel):
    """Respuesta del endpoint /learning-path."""

    total_recommendations: int
    recommendations: list[LearningRecommendation]
