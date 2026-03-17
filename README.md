# Job Insight API

API REST construida con **FastAPI** que analiza descripciones de vacantes de empleo, las compara con el perfil de habilidades de un desarrollador y genera recomendaciones de aprendizaje personalizadas.

---

## Características

- Extracción de habilidades técnicas, soft skills y años de experiencia de texto libre.
- Comparación de perfil vs. vacante con porcentaje de compatibilidad (incluye soft skills).
- Resolución de alias comunes (`postgres` → `postgresql`, `k8s` → `kubernetes`, etc.).
- Generación de rutas de aprendizaje priorizadas con recursos específicos por habilidad.
- Endpoint consolidado para análisis completo en una sola llamada.
- Persistencia en base de datos con transacciones por endpoint.
- Rate limiting por endpoint y CORS configurable por variables de entorno.
- Documentación interactiva automática (Swagger UI y ReDoc).
- Migraciones versionadas con Alembic.

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| Framework | FastAPI 0.115 |
| Servidor ASGI | Uvicorn 0.30 |
| Validación | Pydantic v2 |
| Configuración | pydantic-settings |
| Base de datos | SQLite (local) / PostgreSQL (producción) |
| ORM / DB async | SQLAlchemy 2.0 + aiosqlite / asyncpg |
| Migraciones | Alembic |
| Rate limiting | SlowAPI |
| Testing | Pytest + FastAPI TestClient |
| Lenguaje | Python 3.11+ |

---

## Estructura del proyecto

```
job-insight-api/
├── alembic/                      # Migraciones de base de datos
│   ├── env.py
│   └── versions/
├── app/
│   ├── main.py                      # Inicialización de FastAPI y routers
│   ├── core/
│   │   ├── settings.py              # Configuración centralizada
│   │   └── rate_limiter.py          # Configuración de SlowAPI
│   ├── routers/
│   │   ├── jobs.py                  # Endpoints de vacantes
│   │   └── analysis.py              # Endpoints de matching y recomendaciones
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
│       ├── skill_dictionary.py       # Diccionario de habilidades por categoría
│       └── skill_aliases.py          # Alias canónicos compartidos
├── tests/
│   ├── test_api.py
│   ├── test_matcher.py
│   └── test_skill_extractor.py
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Instalación

### Requisitos previos

- Python 3.11 o superior.
- Entorno virtual recomendado.

### Pasos

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd job-insight-api

# 2. Crear y activar entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. (Opcional) crear archivo .env para personalizar variables
# (el proyecto lee .env automáticamente mediante pydantic-settings)

# 5. Ejecutar migraciones
alembic upgrade head

# 6. Ejecutar el servidor
python -m uvicorn app.main:app --reload
```

El servidor queda disponible en `http://127.0.0.1:8000`.

---

## Producción (Render)

La API ya está desplegada en Render y disponible públicamente.

- Base URL: `https://job-insight-api.onrender.com/`
- Swagger UI: `https://job-insight-api.onrender.com/docs`
- ReDoc: `https://job-insight-api.onrender.com/redoc`

### Variables de entorno recomendadas (producción)

- `PYTHON_VERSION=3.11.9`
- `DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5432/DBNAME`
- `CORS_ALLOW_ORIGINS=["https://tu-frontend.com"]`
- `CORS_ALLOW_CREDENTIALS=false`
- `RATE_LIMIT_ANALYZE_JOB=30/minute`
- `RATE_LIMIT_MATCH_PROFILE=30/minute`
- `RATE_LIMIT_LEARNING_PATH=30/minute`
- `RATE_LIMIT_FULL_REPORT=20/minute`
- `RATE_LIMIT_TRUST_PROXY_HEADERS=false` (activar solo si confías en tu reverse proxy)
- `REQUEST_MAX_DESCRIPTION_LENGTH=10000`

### Variables de entorno clave (desarrollo)

- `DATABASE_URL=sqlite+aiosqlite:///./job_insight.db`
- `DEBUG=false`
- `CORS_ALLOW_ORIGINS=["*"]`
- `CORS_ALLOW_CREDENTIALS=false`

### Nota de base de datos

- **No se recomienda SQLite en producción** en Render.
- Para persistencia estable usa **PostgreSQL** (Render PostgreSQL o externo).

### Migraciones (Alembic)

Este proyecto usa **Alembic** para versionar el esquema de base de datos.

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Crear una nueva migración
alembic revision -m "describe-tu-cambio"

# Revertir una migración
alembic downgrade -1
```

---

## Desarrollo y pruebas

```bash
# Ejecutar tests
python -m pytest -q

# Ejecutar un archivo concreto de tests
python -m pytest tests/test_skill_extractor.py -q
```

---

## Documentación interactiva

| Interfaz | URL |
|---|---|
| Swagger UI (producción) | https://job-insight-api.onrender.com/docs |
| ReDoc (producción) | https://job-insight-api.onrender.com/redoc |
| Swagger UI (local) | http://127.0.0.1:8000/docs |
| ReDoc (local) | http://127.0.0.1:8000/redoc |

---

## Endpoints

### Ejemplo rápido con `curl`

```bash
curl -X POST http://127.0.0.1:8000/analysis/full-report \
  -H "Content-Type: application/json" \
  -d '{
    "profile_skills": ["python", "postgres", "teamwork"],
    "job_description": "We are looking for a Python developer with PostgreSQL, Docker and teamwork."
  }'
```

### `GET /`
Health check de la API.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "Job Insight API is running",
  "version": "1.1.0",
  "database": "up",
  "uptime_seconds": 123
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
  "total_job_skills": 6,
  "matching_soft_skills": ["teamwork"],
  "missing_soft_skills": ["leadership"],
  "total_job_soft_skills": 2
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

---

### `POST /analysis/full-report`
Ejecuta en una sola llamada: análisis de vacante, comparación de perfil y generación de ruta de aprendizaje.

**Request body:**
```json
{
  "profile_skills": ["python", "postgres", "teamwork"],
  "job_description": "We are looking for a Python developer with PostgreSQL, Docker and teamwork."
}
```

**Response (resumen):**
```json
{
  "job_analysis": {"tech_skills": ["docker", "postgresql", "python"], "soft_skills": ["teamwork"], "experience_years": null, "total_skills_found": 4},
  "profile_match": {"compatibility_percentage": 75.0, "matching_skills": ["postgresql", "python"], "missing_skills": ["docker"], "total_job_skills": 3, "matching_soft_skills": ["teamwork"], "missing_soft_skills": [], "total_job_soft_skills": 1},
  "learning_path": {"total_recommendations": 1, "recommendations": [{"skill": "docker", "category": "devops", "priority": "medium", "suggestion": "..."}]}
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

El diccionario cubre habilidades técnicas en 7 categorías:

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

| Alias | Canónico |
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
# Produccion (Render)
BASE_URL="https://job-insight-api.onrender.com"

# Alternativa local
# BASE_URL="http://127.0.0.1:8000"

# 1. Analizar una vacante
curl -X POST "$BASE_URL/jobs/analyze-job" \
  -H "Content-Type: application/json" \
  -d '{"description": "Python developer, 5+ years, Django, Docker, PostgreSQL, AWS required."}'

# 2. Comparar perfil con la vacante
curl -X POST "$BASE_URL/analysis/match-profile" \
  -H "Content-Type: application/json" \
  -d '{"profile_skills": ["python", "django", "postgres"], "job_description": "Python developer, 5+ years, Django, Docker, PostgreSQL, AWS required."}'

# 3. Obtener ruta de aprendizaje para habilidades faltantes
curl -X POST "$BASE_URL/analysis/learning-path" \
  -H "Content-Type: application/json" \
  -d '{"missing_skills": ["docker", "aws"]}'
```
