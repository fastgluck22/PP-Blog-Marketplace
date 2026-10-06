from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.article import Article


async def get_articles(
        session: AsyncSession,
        search: str | None = None,
        category_id: int | None = None,
        page_number: int = 1,
        page_size: int = 10,
):
    query = select(Article).where(
        Article.is_deleted.is_(False)
    )
    if search:
        query = query.where(
            Article.search_vector.op("@@")(
                func.plainto_tsquery("russian", search)
            )
        )

    if category_id:
        query = query.where(
            Article.category_id == category_id
        )

    offset = (page_number - 1) * page_size

    query = query.offset(offset).limit(page_size)

    result = await session.execute(query)

    return result.scalars().all()


async def get_article(
        session: AsyncSession,
        article_id: int,
):
    return await session.get(Article, article_id)


async def create_article(
        session: AsyncSession,
        article: Article,
):
    session.add(article)

    await session.commit()
    await session.refresh(article)

    return article


async def update_article(
        session: AsyncSession,
        article: Article,
):
    await session.commit()
    await session.refresh(article)

    return article


async def delete_article(
        session: AsyncSession,
        article: Article,
):
    await session.commit()
    await session.refresh(article)

    return article