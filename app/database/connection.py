"""Configuracion de conexion a base de datos con SQLAlchemy async."""

from collections.abc import AsyncGenerator

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.settings import settings

DATABASE_URL = settings.database_url

# Render suele entregar postgres:// o postgresql://; para SQLAlchemy async
# convertimos al driver asyncpg.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+asyncpg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=settings.debug)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    """Crea las tablas en la base de datos si no existen."""
    from app.database.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_profile_match_columns(conn)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesiones para inyección de dependencias en FastAPI."""
    async with async_session() as session:
        yield session


async def check_connection() -> bool:
    """Verifica conectividad minima con la base de datos."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def _ensure_profile_match_columns(conn) -> None:
    """Agrega columnas nuevas en instalaciones existentes sin migraciones formales."""

    def _get_columns(sync_conn) -> set[str]:
        inspector = inspect(sync_conn)
        return {col["name"] for col in inspector.get_columns("profile_matches")}

    existing_columns = await conn.run_sync(_get_columns)
    alter_statements: list[str] = []

    if "matching_soft_skills" not in existing_columns:
        alter_statements.append(
            "ALTER TABLE profile_matches ADD COLUMN matching_soft_skills TEXT DEFAULT '[]'"
        )
    if "missing_soft_skills" not in existing_columns:
        alter_statements.append(
            "ALTER TABLE profile_matches ADD COLUMN missing_soft_skills TEXT DEFAULT '[]'"
        )

    for statement in alter_statements:
        await conn.execute(text(statement))
