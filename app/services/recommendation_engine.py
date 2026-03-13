"""Servicio para generar recomendaciones de aprendizaje."""

from app.models.profile_models import LearningRecommendation
from app.utils.skill_dictionary import get_skill_category

# Recursos sugeridos por categoría (fallback cuando no hay recurso específico)
_CATEGORY_RESOURCES: dict[str | None, str] = {
    "languages": "Practica en plataformas como LeetCode, HackerRank o construye proyectos personales.",
    "frameworks": "Sigue el tutorial oficial y construye un proyecto CRUD completo.",
    "databases": "Completa un curso práctico y diseña esquemas para casos de uso reales.",
    "devops": "Configura un pipeline CI/CD personal y despliega un proyecto en la nube.",
    "tools": "Integra la herramienta en tu flujo de trabajo diario con un proyecto real.",
    "data_science": "Trabaja con datasets de Kaggle y reproduce análisis publicados.",
    "testing": "Escribe tests para un proyecto existente y apunta a >80% de cobertura.",
    None: "Busca documentación oficial y tutoriales en línea para comenzar.",
}

# Recursos específicos por skill (tienen precedencia sobre los de categoría)
_SKILL_RESOURCES: dict[str, str] = {
    "python": "Curso: Python docs tutorial → Automate the Boring Stuff → proyectos con FastAPI/Django.",
    "javascript": "Curso: MDN Web Docs → javascript.info → construir una app interactiva.",
    "typescript": "Curso: TypeScript Handbook oficial → migrar un proyecto JS existente a TS.",
    "react": "Curso: react.dev tutorial oficial → construir un dashboard con hooks y context.",
    "django": "Curso: Django docs tutorial → djangoproject.com → proyecto con DRF.",
    "fastapi": "Curso: FastAPI docs tutorial → construir una API REST con auth y DB.",
    "docker": "Curso: Docker docs Get Started → dockerizar un proyecto propio → Docker Compose.",
    "kubernetes": "Curso: Kubernetes.io tutorials → desplegar una app multi-container en Minikube.",
    "aws": "Curso: AWS Skill Builder (gratis) → certificación Cloud Practitioner → labs prácticos.",
    "postgresql": "Curso: PostgreSQL Tutorial oficial → diseñar un esquema normalizado → consultas avanzadas.",
    "git": "Curso: Pro Git book (gratis) → practicar branching, rebasing y resolución de conflictos.",
    "sql": "Curso: SQLBolt o Mode SQL Tutorial → resolver ejercicios con JOINs y subqueries.",
    "mongodb": "Curso: MongoDB University (gratis) → modelar datos para una app real.",
    "redis": "Curso: Redis University → implementar caché y pub/sub en un proyecto.",
    "terraform": "Curso: HashiCorp Learn → definir infra como código para un entorno de staging.",
    "graphql": "Curso: How to GraphQL → construir un API con Apollo Server o Strawberry.",
    "pytest": "Curso: docs de pytest → escribir fixtures, parametrize y plugins para un proyecto.",
}

# Categorías con mayor demanda reciben prioridad alta
_HIGH_PRIORITY_CATEGORIES = {"languages", "frameworks", "databases"}


def generate_learning_path(missing_skills: list[str]) -> list[LearningRecommendation]:
    """Genera recomendaciones de aprendizaje para cada habilidad faltante.

    Cada skill recibe un recurso específico si existe, o uno genérico por
    categoría. Las recomendaciones se ordenan por prioridad (high → low).
    """
    seen: set[str] = set()
    recommendations: list[LearningRecommendation] = []

    for skill in missing_skills:
        normalized = skill.lower().strip()
        if normalized in seen:
            continue
        seen.add(normalized)

        category = get_skill_category(normalized)
        priority = _determine_priority(category)
        suggestion = _get_suggestion(normalized, category)

        recommendations.append(LearningRecommendation(
            skill=normalized,
            category=category,
            priority=priority,
            suggestion=suggestion,
        ))

    # Ordenar: alta prioridad primero
    _PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
    recommendations.sort(key=lambda r: _PRIORITY_ORDER.get(r.priority, 3))

    return recommendations


def _get_suggestion(skill: str, category: str | None) -> str:
    """Retorna el recurso más específico disponible para la habilidad."""
    if skill in _SKILL_RESOURCES:
        return _SKILL_RESOURCES[skill]
    return _CATEGORY_RESOURCES.get(category, _CATEGORY_RESOURCES[None])


def _determine_priority(category: str | None) -> str:
    """Determina la prioridad de aprendizaje según la categoría."""
    if category in _HIGH_PRIORITY_CATEGORIES:
        return "high"
    if category is not None:
        return "medium"
    return "low"
