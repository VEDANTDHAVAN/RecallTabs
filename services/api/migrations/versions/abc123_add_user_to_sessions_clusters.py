"""add user_id to sessions and memory_clusters, unique tab per user+url

Revision ID: abc123
Revises: 611372b65f51
Create Date: 2026-10-27

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'abc123'
down_revision: Union[str, Sequence[str], None] = '611372b65f51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- sessions.user_id ---
    op.add_column('sessions', sa.Column('user_id', sa.String(), nullable=True))
    # backfill from the tabs that belong to each session
    op.execute("""
        UPDATE sessions s
        SET user_id = (
            SELECT t.user_id FROM tabs t
            WHERE t.session_id = s.id
            LIMIT 1
        )
    """)
    # fall back to the first user for orphaned sessions
    op.execute("""
        UPDATE sessions
        SET user_id = (SELECT id FROM users LIMIT 1)
        WHERE user_id IS NULL
    """)
    op.create_foreign_key(
        'fk_sessions_user_id', 'sessions', 'users',
        ['user_id'], ['id'], ondelete='CASCADE',
    )
    op.create_index('ix_sessions_user_id', 'sessions', ['user_id'])
    op.alter_column('sessions', 'user_id', nullable=False)

    # --- memory_clusters.user_id ---
    op.add_column('memory_clusters', sa.Column('user_id', sa.String(), nullable=True))
    # backfill from the sessions that belong to each cluster
    op.execute("""
        UPDATE memory_clusters c
        SET user_id = (
            SELECT s.user_id FROM sessions s
            WHERE s.cluster_id = c.id
            LIMIT 1
        )
    """)
    op.execute("""
        UPDATE memory_clusters
        SET user_id = (SELECT id FROM users LIMIT 1)
        WHERE user_id IS NULL
    """)
    op.create_foreign_key(
        'fk_memory_clusters_user_id', 'memory_clusters', 'users',
        ['user_id'], ['id'], ondelete='CASCADE',
    )
    op.create_index('ix_memory_clusters_user_id', 'memory_clusters', ['user_id'])
    op.alter_column('memory_clusters', 'user_id', nullable=False)

    # --- idempotent capture: one tab per (user, url) ---
    op.create_unique_constraint(
        'uq_tab_user_url', 'tabs', ['user_id', 'url'],
    )


def downgrade() -> None:
    op.drop_constraint('uq_tab_user_url', 'tabs', type_='unique')

    op.drop_column('memory_clusters', 'user_id')
    op.drop_constraint('fk_memory_clusters_user_id', 'memory_clusters', type_='foreignkey')

    op.drop_column('sessions', 'user_id')
    op.drop_constraint('fk_sessions_user_id', 'sessions', type_='foreignkey')
