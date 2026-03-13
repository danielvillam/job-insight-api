"""Router para endpoints de análisis de vacantes."""

from fastapi import APIRouter

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
async def analyze_job(request: JobDescriptionRequest) -> JobAnalysisResponse:
    result = extract_skills(request.description)
    return JobAnalysisResponse(
        tech_skills=result.tech_skills,
        soft_skills=result.soft_skills,
        experience_years=result.experience_years,
        total_skills_found=len(result.tech_skills) + len(result.soft_skills),
    )
