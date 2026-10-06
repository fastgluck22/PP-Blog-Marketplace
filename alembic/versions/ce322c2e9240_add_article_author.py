"""add article author

Revision ID: ce322c2e9240
Revises: 5ec0a6fdcca6
Create Date: 2026-09-25 18:29:31.746844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce322c2e9240'
down_revision: Union[str, Sequence[str], None] = '5ec0a6fdcca6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'articles',
        sa.Column(
            'author_id',
            sa.Integer(),
            nullable=True,
        ),
    )

    op.execute("""
        INSERT INTO users (email, password_hash, role, created_at)
        VALUES (
            'migration@example.com',
            'migration',
            'user',
            NOW()
        )
        ON CONFLICT (email) DO NOTHING
    """)

    op.execute("""
        UPDATE articles
        SET author_id = (
            SELECT id
            FROM users
            WHERE email = 'migration@example.com'
        )
        WHERE author_id IS NULL
    """)

    op.alter_column(
        'articles',
        'author_id',
        nullable=False,
    )

    op.create_foreign_key(
        'fk_articles_author_id_users',
        'articles',
        'users',
        ['author_id'],
        ['id'],
    )

def downgrade() -> None:
    op.drop_constraint(
        'fk_articles_author_id_users',
        'articles',
        type_='foreignkey',
    )

    op.drop_column(
        'articles',
        'author_id',
    )