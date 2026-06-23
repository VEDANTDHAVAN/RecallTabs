"""add cluster embedding

Revision ID: d7d9cced8664
Revises: 4d14f10caddb
Create Date: 2026-06-23 14:57:18.330692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = 'd7d9cced8664'
down_revision: Union[str, Sequence[str], None] = '4d14f10caddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "memory_clusters",
        sa.Column("embedding", Vector(384), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
