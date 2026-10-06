"""add is_deleted to articles

Revision ID: 4c63a0863008
Revises: c1903ef73274
Create Date: 2026-08-30 22:05:47.409430

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c63a0863008'
down_revision: Union[str, Sequence[str], None] = 'c1903ef73274'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'articles',
        sa.Column(
            'is_deleted',
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        )
    )


def downgrade() -> None:
    op.drop_column('articles', 'is_deleted')