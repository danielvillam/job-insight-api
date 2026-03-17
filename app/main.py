import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.rate_limiter import limiter
from app.routers import jobs, analysis
from app.core.settings import settings
from app.database.connection import check_connection, create_tables

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger("job_insight_api")

APP_STARTED_AT = datetime.now(timezone.utc)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Creating database tables if needed")
    await create_tables()
    yield

app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs.router)
app.include_router(analysis.router)


@app.get("/", tags=["health"])
async def root():
    db_ok = await check_connection()
    uptime_seconds = int((datetime.now(timezone.utc) - APP_STARTED_AT).total_seconds())
    return {
        "status": "ok" if db_ok else "degraded",
        "message": "Job Insight API is running",
        "version": settings.app_version,
        "database": "up" if db_ok else "down",
        "uptime_seconds": uptime_seconds,
    }
