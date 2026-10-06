import asyncio

from sqlalchemy import select

from app.core.embedding import create_embedding
from app.db.database import async_session
from app.db.models.article import Article


async def main():
    async with async_session() as session:
        result = await session.execute(
            select(Article).where(
                Article.is_deleted.is_(False)
            )
        )

        articles = result.scalars().all()

        for article in articles:
            print(f"Creating embedding for article {article.id}: {article.title}")

            article.embedding = create_embedding(article.text)

        await session.commit()

        print(f"\nEmbeddings rebuilt for {len(articles)} articles")


if __name__ == "__main__":
    asyncio.run(main())