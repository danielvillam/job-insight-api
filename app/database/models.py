"""Modelos SQLAlchemy para persistencia."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class JobAnalysis(Base):
    """Registro de análisis de vacantes realizados."""

    __tablename__ = "job_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description_hash = Column(String(64), index=True)
    tech_skills = Column(Text)
    soft_skills = Column(Text)
    experience_years = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class ProfileMatch(Base):
    """Registro de comparaciones perfil-vacante."""

    __tablename__ = "profile_matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    compatibility_percentage = Column(Float)
    matching_skills = Column(Text)
    missing_skills = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
