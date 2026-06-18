"""add ai metadata to tabs

Revision ID: 5d7137fb83ce
Revises: 95ddee540a81
Create Date: 2026-06-18 17:48:01.929374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d7137fb83ce'
down_revision: Union[str, Sequence[str], None] = '95ddee540a81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "tabs", sa.Column("summary", sa.Text(), nullable=True)
    )

    op.add_column(
        "tabs", sa.Column("keywords", sa.JSON(), nullable=True)
    )

    op.add_column(
        "tabs", sa.Column("topic", sa.String(), nullable=True)
    )

    op.add_column(
        "tabs", sa.Column("category", sa.String(), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
