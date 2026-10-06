"""add user role

Revision ID: 5ec0a6fdcca6
Revises: 3e71fd75f415
Create Date: 2026-09-25 18:21:53.091507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ec0a6fdcca6'
down_revision: Union[str, Sequence[str], None] = '3e71fd75f415'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column(
            'role',
            sa.String(length=30),
            nullable=False,
            server_default='user',
        ),
    )


def downgrade() -> None:
    op.drop_column('users', 'role')