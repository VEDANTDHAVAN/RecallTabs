"""create memory clusters

Revision ID: 4d14f10caddb
Revises: 377c0e08b827
Create Date: 2026-06-23 14:16:25.277418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '4d14f10caddb'
down_revision: Union[str, Sequence[str], None] = '377c0e08b827'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("memory_clusters", 
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
    )

    op.add_column("sessions",
        sa.Column("cluster_id", sa.String(), nullable=True)
    )

    op.create_foreign_key(
        "fk_sessions_cluster", "sessions",
        "memory_clusters", ["cluster_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
