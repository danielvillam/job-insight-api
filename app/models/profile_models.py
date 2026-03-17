"""Modelos Pydantic para perfiles y comparación."""

from pydantic import BaseModel, Field

from app.core.settings import settings
from app.models.job_models import JobAnalysisResponse


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
        max_length=settings.request_max_description_length,
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
    matching_soft_skills: list[str] = Field(default_factory=list)
    missing_soft_skills: list[str] = Field(default_factory=list)
    total_job_soft_skills: int = 0


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


class FullAnalysisRequest(BaseModel):
    """Cuerpo de la peticion para analisis completo en una sola llamada."""

    profile_skills: list[str] = Field(
        ...,
        min_length=1,
        examples=[["python", "django", "docker", "postgresql"]],
        description="Lista de habilidades del perfil del desarrollador.",
    )
    job_description: str = Field(
        ...,
        min_length=20,
        max_length=settings.request_max_description_length,
        description="Texto completo de la descripcion de la vacante.",
    )


class FullAnalysisResponse(BaseModel):
    """Respuesta consolidada con analisis, matching y ruta de aprendizaje."""

    job_analysis: JobAnalysisResponse
    profile_match: MatchProfileResponse
    learning_path: LearningPathResponse
