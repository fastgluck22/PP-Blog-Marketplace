"""add article embedding

Revision ID: 3e5b751082ba
Revises: 9c0176fd8154
Create Date: 2026-10-04 16:30:50.052288

"""
from typing import Sequence, Union
from pgvector.sqlalchemy import VECTOR
from alembic import op
import sqlalchemy as sa


revision: str = '3e5b751082ba'
down_revision: Union[str, Sequence[str], None] = '9c0176fd8154'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'articles',
        sa.Column(
            'embedding',
            VECTOR(dim=384),
            nullable=True,
        ),
    )

def downgrade() -> None:
    op.drop_column('articles', 'embedding')
