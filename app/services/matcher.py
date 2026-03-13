"""Servicio para comparar perfiles de desarrollador con vacantes."""

from app.services.skill_extractor import extract_skills, _ALIASES


def _normalize_skill(skill: str) -> str:
    """Normaliza una habilidad resolviendo alias a su forma canónica."""
    lowered = skill.lower().strip()
    return _ALIASES.get(lowered, lowered)


def match_profile(profile_skills: list[str], job_description: str) -> dict:
    """Compara las habilidades del perfil con las requeridas en la vacante.

    Normaliza ambas listas (perfil y vacante) para que alias como
    "postgres" y "postgresql" se traten como la misma habilidad.

    Returns:
        dict con compatibility_percentage, matching_skills,
        missing_skills y total_job_skills.
    """
    extracted = extract_skills(job_description)
    job_skills = set(extracted.tech_skills)

    # Normalizar habilidades del perfil resolviendo alias
    profile_set = {_normalize_skill(s) for s in profile_skills}

    matching = sorted(job_skills & profile_set)
    missing = sorted(job_skills - profile_set)

    total = len(job_skills)
    percentage = (len(matching) / total * 100) if total > 0 else 0.0

    return {
        "compatibility_percentage": round(percentage, 1),
        "matching_skills": matching,
        "missing_skills": missing,
        "total_job_skills": total,
    }
