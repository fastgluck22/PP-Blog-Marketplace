"""add search vector to articles

Revision ID: 3e71fd75f415
Revises: 4c63a0863008
Create Date: 2026-09-08 18:13:09.591866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '3e71fd75f415'
down_revision: Union[str, Sequence[str], None] = '4c63a0863008'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.add_column(
            'articles',
            sa.Column(
                'search_vector',
                postgresql.TSVECTOR(),
                nullable=True,
            ),
        )

        op.execute("""
            UPDATE articles
            SET search_vector =
                to_tsvector(
                    'russian',
                    coalesce(title, '') || ' ' || coalesce(text, '')
                )
        """)

        op.create_index(
            'ix_articles_search_vector',
            'articles',
            ['search_vector'],
            postgresql_using='gin',
        )



def downgrade() -> None:
        op.drop_index(
            'ix_articles_search_vector',
            table_name='articles',
        )

        op.drop_column(
            'articles',
            'search_vector',
        )
