from fastapi import FastAPI

from app.routers import jobs, analysis
from app.database.connection import create_tables

app = FastAPI(
    title="Job Insight API",
    description=(
        "API para analizar descripciones de vacantes de empleo, "
        "compararlas con perfiles de desarrolladores y generar "
        "recomendaciones de aprendizaje."
    ),
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    await create_tables()


app.include_router(jobs.router)
app.include_router(analysis.router)


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "Job Insight API is running"}
