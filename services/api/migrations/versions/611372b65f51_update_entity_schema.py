"""update entity schema

Revision ID: 611372b65f51
Revises: bf7bf42cbc00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "611372b65f51"
down_revision: Union[str, Sequence[str], None] = "bf7bf42cbc00"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename summary -> description (preserves existing data)
    op.alter_column(
        "entities",
        "summary",
        new_column_name="description",
        existing_type=sa.String(),
        existing_nullable=True,
    )

    # Add new columns with safe defaults
    op.add_column(
        "entities",
        sa.Column(
            "confidence",
            sa.Float(),
            nullable=False,
            server_default="1.0",
        ),
    )

    op.add_column(
        "entities",
        sa.Column(
            "mention_count",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),
    )

    op.add_column(
        "entities",
        sa.Column(
            "last_seen_at",
            sa.DateTime(),
            nullable=True,
        ),
    )

    # Remove temporary defaults so future inserts use the ORM defaults
    op.alter_column(
        "entities",
        "confidence",
        server_default=None,
    )

    op.alter_column(
        "entities",
        "mention_count",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("entities", "last_seen_at")
    op.drop_column("entities", "mention_count")
    op.drop_column("entities", "confidence")

    op.alter_column(
        "entities",
        "description",
        new_column_name="summary",
        existing_type=sa.Text(),
        existing_nullable=True,
    )