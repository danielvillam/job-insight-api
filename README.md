# Job Insight API

API REST construida con **FastAPI** que analiza descripciones de vacantes de empleo, las compara con el perfil de habilidades de un desarrollador y genera recomendaciones de aprendizaje personalizadas.

---

## Características

- Extracción de habilidades técnicas, soft skills y años de experiencia de texto libre.
- Comparación de perfil vs. vacante con porcentaje de compatibilidad.
- Resolución de alias comunes (`postgres` → `postgresql`, `k8s` → `kubernetes`, etc.).
- Generación de rutas de aprendizaje priorizadas con recursos específicos por habilidad.
- Documentación interactiva automática (Swagger UI y ReDoc).
- Base de datos SQLite async con SQLAlchemy.

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| Framework | FastAPI 0.115 |
| Servidor ASGI | Uvicorn 0.30 |
| Validación | Pydantic v2 |
| Base de datos | SQLite (aiosqlite) |
| ORM | SQLAlchemy 2.0 async |
| Lenguaje | Python 3.11+ |

---

## Estructura del proyecto

```
job-insight-api/
├── app/
│   ├── main.py                      # Inicialización de FastAPI y routers
│   ├── routers/
│   │   ├── jobs.py                  # POST /jobs/analyze-job
│   │   └── analysis.py             # POST /analysis/match-profile
│   │                                #  POST /analysis/learning-path
│   ├── services/
│   │   ├── skill_extractor.py       # Extracción de habilidades con regex
│   │   ├── matcher.py               # Comparación perfil vs. vacante
│   │   └── recommendation_engine.py # Generación de rutas de aprendizaje
│   ├── models/
│   │   ├── job_models.py            # Modelos Pydantic para vacantes
│   │   └── profile_models.py        # Modelos Pydantic para perfiles
│   ├── database/
│   │   ├── connection.py            # Engine async y sesión SQLAlchemy
│   │   └── models.py                # Tablas SQLAlchemy (JobAnalysis, ProfileMatch)
│   └── utils/
│       └── skill_dictionary.py      # Diccionario de 100+ habilidades técnicas
├── requirements.txt
└── README.md
```

---

## Instalación

### Requisitos previos

- Python 3.11 o superior.

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/job-insight-api.git
cd job-insight-api

# 2. Crear y activar entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servidor
python -m uvicorn app.main:app --reload
```

El servidor queda disponible en `http://127.0.0.1:8000`.

---

## Documentación interactiva

| Interfaz | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |

---

## Endpoints

### `GET /`
Health check de la API.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Job Insight API is running"
}
```

---

### `POST /jobs/analyze-job`
Analiza el texto de una oferta laboral y devuelve habilidades detectadas, años de experiencia y soft skills.

**Request body:**
```json
{
  "description": "We are looking for a Python developer with 3+ years of experience in Django and REST APIs. Knowledge of Docker and PostgreSQL is a plus. Teamwork and agile methodology required."
}
```

**Response:**
```json
{
  "tech_skills": ["django", "docker", "postgresql", "python", "rest"],
  "soft_skills": ["agile", "teamwork"],
  "experience_years": 3,
  "total_skills_found": 7
}
```

---

### `POST /analysis/match-profile`
Compara las habilidades de un desarrollador con las requeridas en una vacante y calcula la compatibilidad.

**Request body:**
```json
{
  "profile_skills": ["python", "django", "git", "postgres"],
  "job_description": "We need a Python developer with Django, Docker, PostgreSQL, and AWS experience."
}
```

> Los alias se resuelven automáticamente: `postgres` equivale a `postgresql`, `k8s` a `kubernetes`, etc.

**Response:**
```json
{
  "compatibility_percentage": 50.0,
  "matching_skills": ["django", "postgresql", "python"],
  "missing_skills": ["aws", "docker"],
  "total_job_skills": 6
}
```

---

### `POST /analysis/learning-path`
Genera recomendaciones de aprendizaje priorizadas para cada habilidad faltante.

**Request body:**
```json
{
  "missing_skills": ["docker", "postgresql", "aws"]
}
```

**Response:**
```json
{
  "total_recommendations": 3,
  "recommendations": [
    {
      "skill": "postgresql",
      "category": "databases",
      "priority": "high",
      "suggestion": "Curso: PostgreSQL Tutorial oficial → diseñar un esquema normalizado → consultas avanzadas."
    },
    {
      "skill": "docker",
      "category": "devops",
      "priority": "medium",
      "suggestion": "Curso: Docker docs Get Started → dockerizar un proyecto propio → Docker Compose."
    },
    {
      "skill": "aws",
      "category": "devops",
      "priority": "medium",
      "suggestion": "Curso: AWS Skill Builder (gratis) → certificación Cloud Practitioner → labs prácticos."
    }
  ]
}
```

Las recomendaciones se ordenan por prioridad (`high` → `medium` → `low`), determinada según la categoría de la habilidad:

| Prioridad | Categorías |
|---|---|
| `high` | languages, frameworks, databases |
| `medium` | devops, tools, data_science, testing |
| `low` | habilidades no reconocidas |

---

## Habilidades detectadas

El diccionario cubre más de 100 habilidades en 7 categorías:

| Categoría | Ejemplos |
|---|---|
| **languages** | Python, JavaScript, TypeScript, Java, Go, Rust, SQL |
| **frameworks** | Django, FastAPI, React, Angular, Vue, Spring Boot |
| **databases** | PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch |
| **devops** | Docker, Kubernetes, AWS, Azure, Terraform, GitHub Actions |
| **tools** | Git, GraphQL, Kafka, Swagger, REST, gRPC |
| **data_science** | Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch |
| **testing** | Pytest, Jest, Cypress, Selenium |

### Alias soportados

| Alias | Canonico |
|---|---|
| `node`, `node.js` | `nodejs` |
| `react.js`, `reactjs` | `react` |
| `postgres` | `postgresql` |
| `mongo` | `mongodb` |
| `k8s` | `kubernetes` |
| `sklearn` | `scikit-learn` |
| `js` | `javascript` |
| `ts` | `typescript` |
| `csharp`, `c sharp` | `c#` |
| `dotnet` | `.net` |
| `gh actions` | `github actions` |

---

## Ejemplo completo de flujo

```bash
# 1. Analizar una vacante
curl -X POST http://127.0.0.1:8000/jobs/analyze-job \
  -H "Content-Type: application/json" \
  -d '{"description": "Python developer, 5+ years, Django, Docker, PostgreSQL, AWS required."}'

# 2. Comparar perfil con la vacante
curl -X POST http://127.0.0.1:8000/analysis/match-profile \
  -H "Content-Type: application/json" \
  -d '{"profile_skills": ["python", "django", "postgres"], "job_description": "Python developer, 5+ years, Django, Docker, PostgreSQL, AWS required."}'

# 3. Obtener ruta de aprendizaje para habilidades faltantes
curl -X POST http://127.0.0.1:8000/analysis/learning-path \
  -H "Content-Type: application/json" \
  -d '{"missing_skills": ["docker", "aws"]}'
```
