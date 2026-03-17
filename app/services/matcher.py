"""Servicio para comparar perfiles de desarrollador con vacantes."""

from typing import TypedDict

from app.models.job_models import ExtractedSkills
from app.services.skill_extractor import extract_skills
from app.utils.skill_aliases import normalize_skill


class MatchResult(TypedDict):
    compatibility_percentage: float
    matching_skills: list[str]
    missing_skills: list[str]
    total_job_skills: int
    matching_soft_skills: list[str]
    missing_soft_skills: list[str]
    total_job_soft_skills: int


def match_profile(
    profile_skills: list[str],
    job_description: str,
    extracted: ExtractedSkills | None = None,
) -> MatchResult:
    """Compara las habilidades del perfil con las requeridas en la vacante.

    Normaliza ambas listas (perfil y vacante) para que alias como
    "postgres" y "postgresql" se traten como la misma habilidad.

    Returns:
        dict con compatibility_percentage, matching_skills,
        missing_skills y total_job_skills.
    """
    extracted_result = extracted or extract_skills(job_description)
    job_skills = set(extracted_result.tech_skills)
    job_soft_skills = set(extracted_result.soft_skills)

    # Normalizar habilidades del perfil resolviendo alias
    profile_set = {normalize_skill(s) for s in profile_skills}

    matching = sorted(job_skills & profile_set)
    missing = sorted(job_skills - profile_set)
    matching_soft = sorted(job_soft_skills & profile_set)
    missing_soft = sorted(job_soft_skills - profile_set)

    total_tech = len(job_skills)
    total_soft = len(job_soft_skills)
    total_required = total_tech + total_soft
    total_matched = len(matching) + len(matching_soft)
    percentage = (total_matched / total_required * 100) if total_required > 0 else 0.0

    return {
        "compatibility_percentage": round(percentage, 1),
        "matching_skills": matching,
        "missing_skills": missing,
        "total_job_skills": total_tech,
        "matching_soft_skills": matching_soft,
        "missing_soft_skills": missing_soft,
        "total_job_soft_skills": total_soft,
    }
