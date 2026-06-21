"""create tab relationships

Revision ID: 4bf54ca1de4d
Revises: 5d7137fb83ce
Create Date: 2026-06-18 19:03:52.777780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4bf54ca1de4d'
down_revision: Union[str, Sequence[str], None] = '5d7137fb83ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tab_relationships",
        sa.Column(
            "id",
            sa.String(),
            primary_key=True
        ),
        sa.Column(
            "source_tab_id",
            sa.String(),
            sa.ForeignKey("tabs.id")
        ),
        sa.Column(
            "related_tab_id",
            sa.String(),
            sa.ForeignKey("tabs.id")
        ),
        sa.Column(
            "similarity_score",
            sa.Float()
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
