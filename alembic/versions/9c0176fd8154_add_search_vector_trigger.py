"""add search vector trigger

Revision ID: 9c0176fd8154
Revises: ce322c2e9240
Create Date: 2026-09-30 15:02:51.100082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c0176fd8154'
down_revision: Union[str, Sequence[str], None] = 'ce322c2e9240'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE FUNCTION articles_search_vector_update()
        RETURNS trigger AS $$
        BEGIN
            NEW.search_vector :=
                to_tsvector(
                    'russian',
                    coalesce(NEW.title, '') || ' ' || coalesce(NEW.text, '')
                );

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        CREATE TRIGGER articles_search_vector_trigger
        BEFORE INSERT OR UPDATE OF title, text
        ON articles
        FOR EACH ROW
        EXECUTE FUNCTION articles_search_vector_update();
    """)


def downgrade() -> None:
    op.execute("""
            DROP TRIGGER IF EXISTS articles_search_vector_trigger
            ON articles;
         """)

    op.execute("""
            DROP FUNCTION IF EXISTS articles_search_vector_update();
        """)