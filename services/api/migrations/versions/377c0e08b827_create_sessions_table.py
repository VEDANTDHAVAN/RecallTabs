"""create sessions table

Revision ID: 377c0e08b827
Revises: 4bf54ca1de4d
Create Date: 2026-06-22 22:48:10.646616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '377c0e08b827'
down_revision: Union[str, Sequence[str], None] = '4bf54ca1de4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("topic", sa.String(255), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
    )

    op.add_column(
        "tabs", sa.Column("session_id", sa.String(), nullable=True)
    )

    op.create_foreign_key(
        "fk_tabs_session", "tabs", "sessions",
        ["session_id"], ["id"],
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "fk_tabs_session", "tabs", type_="foreignkey"
    )

    op.drop_column(
        "tabs",
        "session_id"
    )

    op.drop_table(
        "sessions"
    )
