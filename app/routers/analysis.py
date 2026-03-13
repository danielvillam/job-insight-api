"""Router para endpoints de comparación de perfil y ruta de aprendizaje."""

from fastapi import APIRouter

from app.models.profile_models import (
    LearningPathRequest,
    LearningPathResponse,
    MatchProfileRequest,
    MatchProfileResponse,
)
from app.services.matcher import match_profile
from app.services.recommendation_engine import generate_learning_path

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post(
    "/match-profile",
    response_model=MatchProfileResponse,
    summary="Comparar perfil con vacante",
    description="Recibe habilidades del perfil y descripción de vacante. "
                "Devuelve porcentaje de compatibilidad y habilidades faltantes.",
)
async def match(request: MatchProfileRequest) -> MatchProfileResponse:
    result = match_profile(request.profile_skills, request.job_description)
    return MatchProfileResponse(**result)


@router.post(
    "/learning-path",
    response_model=LearningPathResponse,
    summary="Generar ruta de aprendizaje",
    description="Devuelve recomendaciones de aprendizaje basadas en habilidades faltantes.",
)
async def learning_path(request: LearningPathRequest) -> LearningPathResponse:
    recommendations = generate_learning_path(request.missing_skills)
    return LearningPathResponse(
        total_recommendations=len(recommendations),
        recommendations=recommendations,
    )
