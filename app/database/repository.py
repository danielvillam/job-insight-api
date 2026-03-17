"""Operaciones de persistencia para analisis y matching."""

import hashlib
import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import JobAnalysis, ProfileMatch


def hash_description(description: str) -> str:
    """Genera un hash deterministico de la descripcion de vacante."""
    return hashlib.sha256(description.encode("utf-8")).hexdigest()


async def save_job_analysis(
    session: AsyncSession,
    description: str,
    tech_skills: list[str],
    soft_skills: list[str],
    experience_years: int | None,
) -> JobAnalysis:
    """Guarda un analisis de vacante en la base de datos."""
    record = JobAnalysis(
        description_hash=hash_description(description),
        tech_skills=json.dumps(tech_skills),
        soft_skills=json.dumps(soft_skills),
        experience_years=experience_years,
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record


async def save_profile_match(
    session: AsyncSession,
    compatibility_percentage: float,
    matching_skills: list[str],
    missing_skills: list[str],
    matching_soft_skills: list[str],
    missing_soft_skills: list[str],
) -> ProfileMatch:
    """Guarda una comparacion perfil-vacante en la base de datos."""
    record = ProfileMatch(
        compatibility_percentage=compatibility_percentage,
        matching_skills=json.dumps(matching_skills),
        missing_skills=json.dumps(missing_skills),
        matching_soft_skills=json.dumps(matching_soft_skills),
        missing_soft_skills=json.dumps(missing_soft_skills),
    )
    session.add(record)
    await session.commit()
    await session.refresh(record)
    return record
