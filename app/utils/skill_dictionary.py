"""Diccionario centralizado de habilidades técnicas y soft skills."""

# Habilidades técnicas organizadas por categoría
TECH_SKILLS: dict[str, list[str]] = {
    "languages": [
        "python", "javascript", "typescript", "java", "c#", "c++", "go",
        "rust", "ruby", "php", "swift", "kotlin", "scala", "r", "sql",
        "html", "css", "sass", "less",
    ],
    "frameworks": [
        "django", "flask", "fastapi", "spring", "spring boot", "express",
        "nestjs", "react", "angular", "vue", "svelte", "next.js", "nuxt",
        "rails", "laravel", "asp.net", ".net",
    ],
    "databases": [
        "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
        "sqlite", "oracle", "sql server", "dynamodb", "cassandra",
        "firebase", "supabase",
    ],
    "devops": [
        "docker", "kubernetes", "jenkins", "github actions", "gitlab ci",
        "terraform", "ansible", "aws", "azure", "gcp", "ci/cd", "linux",
        "nginx",
    ],
    "tools": [
        "git", "jira", "confluence", "figma", "postman", "swagger",
        "graphql", "rest", "grpc", "kafka", "rabbitmq", "celery",
    ],
    "data_science": [
        "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "keras", "matplotlib", "spark", "airflow", "dbt",
    ],
    "testing": [
        "pytest", "unittest", "jest", "cypress", "selenium",
        "junit", "mocha",
    ],
}

SOFT_SKILLS: list[str] = [
    "communication", "comunicación",
    "teamwork", "trabajo en equipo",
    "leadership", "liderazgo",
    "problem solving", "resolución de problemas",
    "critical thinking", "pensamiento crítico",
    "time management", "gestión del tiempo",
    "adaptability", "adaptabilidad",
    "creativity", "creatividad",
    "proactive", "proactivo",
    "self-taught", "autodidacta",
    "attention to detail", "atención al detalle",
    "collaboration", "colaboración",
    "mentoring", "mentoría",
    "agile", "scrum", "kanban",
]

# Patrones para detectar años de experiencia
EXPERIENCE_PATTERNS: list[str] = [
    r"(\d+)\+?\s*(?:years?|años?)\s*(?:of\s*)?(?:experience|experiencia)",
    r"(?:experience|experiencia)\s*(?:of\s*)?(\d+)\+?\s*(?:years?|años?)",
    r"(\d+)\+?\s*(?:years?|años?)",
    r"(?:at least|al menos|mínimo)\s*(\d+)\s*(?:years?|años?)",
]


def get_all_tech_skills() -> list[str]:
    """Retorna una lista plana con todas las habilidades técnicas."""
    skills: list[str] = []
    for category_skills in TECH_SKILLS.values():
        skills.extend(category_skills)
    return skills


def get_skill_category(skill: str) -> str | None:
    """Retorna la categoría a la que pertenece una habilidad."""
    skill_lower = skill.lower()
    for category, skills in TECH_SKILLS.items():
        if skill_lower in skills:
            return category
    return None
