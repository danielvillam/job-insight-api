"""Router para endpoints de análisis de vacantes."""

import asyncio

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limiter import limiter
from app.core.settings import settings
from app.database.connection import get_session
from app.database.repository import save_job_analysis
from app.models.job_models import JobDescriptionRequest, JobAnalysisResponse
from app.services.skill_extractor import extract_skills

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post(
    "/analyze-job",
    response_model=JobAnalysisResponse,
    summary="Analizar una oferta laboral",
    description="Recibe el texto de una vacante y devuelve habilidades detectadas, "
                "años de experiencia y soft skills.",
)
@limiter.limit(settings.rate_limit_analyze_job)
async def analyze_job(
    request: Request,
    payload: JobDescriptionRequest,
    session: AsyncSession = Depends(get_session),
) -> JobAnalysisResponse:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, extract_skills, payload.description)

    await save_job_analysis(
        session=session,
        description=payload.description,
        tech_skills=result.tech_skills,
        soft_skills=result.soft_skills,
        experience_years=result.experience_years,
    )
    await session.commit()

    return JobAnalysisResponse(
        tech_skills=result.tech_skills,
        soft_skills=result.soft_skills,
        experience_years=result.experience_years,
        total_skills_found=len(result.tech_skills) + len(result.soft_skills),
    )
