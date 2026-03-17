"""Router para endpoints de comparación de perfil y ruta de aprendizaje."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limiter import limiter
from app.core.settings import settings
from app.database.connection import get_session
from app.database.repository import save_job_analysis, save_profile_match
from app.models.job_models import JobAnalysisResponse
from app.models.profile_models import (
    FullAnalysisRequest,
    FullAnalysisResponse,
    LearningPathRequest,
    LearningPathResponse,
    MatchProfileRequest,
    MatchProfileResponse,
)
from app.services.matcher import match_profile
from app.services.recommendation_engine import generate_learning_path
from app.services.skill_extractor import extract_skills

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post(
    "/match-profile",
    response_model=MatchProfileResponse,
    summary="Comparar perfil con vacante",
    description="Recibe habilidades del perfil y descripción de vacante. "
                "Devuelve porcentaje de compatibilidad y habilidades faltantes.",
)
@limiter.limit(settings.rate_limit_match_profile)
async def match(
    request: Request,
    payload: MatchProfileRequest,
    session: AsyncSession = Depends(get_session),
) -> MatchProfileResponse:
    result = match_profile(payload.profile_skills, payload.job_description)

    await save_profile_match(
        session=session,
        compatibility_percentage=result["compatibility_percentage"],
        matching_skills=result["matching_skills"],
        missing_skills=result["missing_skills"],
        matching_soft_skills=result["matching_soft_skills"],
        missing_soft_skills=result["missing_soft_skills"],
    )
    await session.commit()

    return MatchProfileResponse(**result)


@router.post(
    "/learning-path",
    response_model=LearningPathResponse,
    summary="Generar ruta de aprendizaje",
    description="Devuelve recomendaciones de aprendizaje basadas en habilidades faltantes.",
)
@limiter.limit(settings.rate_limit_learning_path)
async def learning_path(request: Request, payload: LearningPathRequest) -> LearningPathResponse:
    recommendations = generate_learning_path(payload.missing_skills)
    return LearningPathResponse(
        total_recommendations=len(recommendations),
        recommendations=recommendations,
    )


@router.post(
    "/full-report",
    response_model=FullAnalysisResponse,
    summary="Generar reporte completo",
    description="Ejecuta analisis de vacante, matching de perfil y ruta de aprendizaje en una sola llamada.",
)
@limiter.limit(settings.rate_limit_full_report)
async def full_report(
    request: Request,
    payload: FullAnalysisRequest,
    session: AsyncSession = Depends(get_session),
) -> FullAnalysisResponse:
    extracted = extract_skills(payload.job_description)
    match_result = match_profile(
        payload.profile_skills,
        payload.job_description,
        extracted,
    )
    recommendations = generate_learning_path(match_result["missing_skills"])

    await save_job_analysis(
        session=session,
        description=payload.job_description,
        tech_skills=extracted.tech_skills,
        soft_skills=extracted.soft_skills,
        experience_years=extracted.experience_years,
    )
    await save_profile_match(
        session=session,
        compatibility_percentage=match_result["compatibility_percentage"],
        matching_skills=match_result["matching_skills"],
        missing_skills=match_result["missing_skills"],
        matching_soft_skills=match_result["matching_soft_skills"],
        missing_soft_skills=match_result["missing_soft_skills"],
    )
    await session.commit()

    return FullAnalysisResponse(
        job_analysis=JobAnalysisResponse(
            tech_skills=extracted.tech_skills,
            soft_skills=extracted.soft_skills,
            experience_years=extracted.experience_years,
            total_skills_found=len(extracted.tech_skills) + len(extracted.soft_skills),
        ),
        profile_match=MatchProfileResponse(**match_result),
        learning_path=LearningPathResponse(
            total_recommendations=len(recommendations),
            recommendations=recommendations,
        ),
    )
