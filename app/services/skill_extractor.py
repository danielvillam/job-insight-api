"""Servicio para extraer habilidades de texto de descripciones de vacantes."""

import re

from app.utils.skill_dictionary import (
    EXPERIENCE_PATTERNS,
    SOFT_SKILLS,
    get_all_tech_skills,
)
from app.models.job_models import ExtractedSkills

# Alias → nombre canónico. Permite detectar variaciones comunes.
_ALIASES: dict[str, str] = {
    "node.js": "nodejs",
    "node": "nodejs",
    "react.js": "react",
    "reactjs": "react",
    "vue.js": "vue",
    "vuejs": "vue",
    "angular.js": "angular",
    "angularjs": "angular",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "k8s": "kubernetes",
    "tf": "terraform",
    "js": "javascript",
    "ts": "typescript",
    "c sharp": "c#",
    "csharp": "c#",
    "dotnet": ".net",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "gh actions": "github actions",
}


def _compile_patterns() -> list[tuple[re.Pattern[str], str]]:
    """Pre-compila patrones regex para cada skill y alias (se ejecuta una sola vez)."""
    patterns: list[tuple[re.Pattern[str], str]] = []

    # Patrones para habilidades del diccionario principal
    for skill in get_all_tech_skills():
        pat = re.compile(rf"\b{re.escape(skill)}\b", re.IGNORECASE)
        patterns.append((pat, skill))

    # Patrones para alias → nombre canónico
    for alias, canonical in _ALIASES.items():
        pat = re.compile(rf"\b{re.escape(alias)}\b", re.IGNORECASE)
        patterns.append((pat, canonical))

    return patterns


# Compilar una sola vez al importar el módulo
_TECH_PATTERNS = _compile_patterns()
_SOFT_PATTERNS = [
    (re.compile(rf"\b{re.escape(s)}\b", re.IGNORECASE), s)
    for s in SOFT_SKILLS
]
_EXP_PATTERNS = [re.compile(p, re.IGNORECASE) for p in EXPERIENCE_PATTERNS]


def extract_skills(text: str) -> ExtractedSkills:
    """Analiza un texto y extrae habilidades técnicas, soft skills y experiencia."""
    tech_skills = _extract_tech_skills(text)
    soft_skills = _extract_soft_skills(text)
    experience_years = _extract_experience(text)

    return ExtractedSkills(
        tech_skills=sorted(tech_skills),
        soft_skills=sorted(soft_skills),
        experience_years=experience_years,
    )


def _extract_tech_skills(text: str) -> list[str]:
    """Busca habilidades técnicas dentro del texto sin duplicados."""
    found: set[str] = set()
    for pattern, canonical in _TECH_PATTERNS:
        if pattern.search(text):
            found.add(canonical)
    return list(found)


def _extract_soft_skills(text: str) -> list[str]:
    """Busca soft skills dentro del texto sin duplicados."""
    found: set[str] = set()
    for pattern, skill in _SOFT_PATTERNS:
        if pattern.search(text):
            found.add(skill)
    return list(found)


def _extract_experience(text: str) -> int | None:
    """Extrae años de experiencia del texto. Retorna el primer valor encontrado."""
    for pattern in _EXP_PATTERNS:
        match = pattern.search(text)
        if match:
            return int(match.group(1))
    return None
