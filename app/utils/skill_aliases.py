"""Alias compartidos para normalizacion de habilidades."""

SKILL_ALIASES: dict[str, str] = {
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
    "js": "javascript",
    "ts": "typescript",
    "c sharp": "c#",
    "csharp": "c#",
    "dotnet": ".net",
    "scikit learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "gh actions": "github actions",
}


def normalize_skill(skill: str) -> str:
    """Normaliza una habilidad resolviendo alias a su forma canonica."""
    lowered = skill.lower().strip()
    return SKILL_ALIASES.get(lowered, lowered)
