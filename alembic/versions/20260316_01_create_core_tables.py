"""create core tables

Revision ID: 20260316_01
Revises:
Create Date: 2026-03-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260316_01"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_analyses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description_hash", sa.String(length=64), nullable=False),
        sa.Column("tech_skills", sa.Text(), nullable=True),
        sa.Column("soft_skills", sa.Text(), nullable=True),
        sa.Column("experience_years", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_job_analyses_description_hash",
        "job_analyses",
        ["description_hash"],
        unique=False,
    )

    op.create_table(
        "profile_matches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("compatibility_percentage", sa.Float(), nullable=True),
        sa.Column("matching_skills", sa.Text(), nullable=True),
        sa.Column("missing_skills", sa.Text(), nullable=True),
        sa.Column("matching_soft_skills", sa.Text(), nullable=True, server_default="[]"),
        sa.Column("missing_soft_skills", sa.Text(), nullable=True, server_default="[]"),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("profile_matches")
    op.drop_index("ix_job_analyses_description_hash", table_name="job_analyses")
    op.drop_table("job_analyses")
