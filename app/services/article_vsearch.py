from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.article import Article
from app.core.embedding import create_embedding

async def search_articles(
        question: str,
        session: AsyncSession,
        limit: int = 3
):
        question_embedding = create_embedding(question)

        distance = Article.embedding.cosine_distance(question_embedding)

        query = (
            select(Article, distance)
            .where(
                Article.is_deleted.is_(False),
                Article.embedding.is_not(None),
            )
            .order_by(distance)
            .limit(limit)
        )

        result = await session.execute(query)

        return result.all()