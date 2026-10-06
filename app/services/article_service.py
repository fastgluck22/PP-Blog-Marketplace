from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User

from app.db.models.article import Article
from app.repositories import article_repository
from app.rabbitmq.producer import publish_message

async def create_article(
        session: AsyncSession,
        article: Article,
) -> Article:
    article = await article_repository.create_article(
        session=session,
        article=article,
    )

    await publish_message(
        "article_embedding",
        {"article_id": article.id, "text": article.text,
         },
    )

    return article


async def update_article(
        session: AsyncSession,
        article_id: int,
        user: User,
        title: str,
        text: str,
        image: str,
        category_id: int,
) -> Article:

    article = await article_repository.get_article(
        session,
        article_id,
    )

    if not article or article.is_deleted:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    if user.role != "admin" and article.author_id != user.id:
        raise HTTPException(
            status_code=403,
        )

    article.title = title
    article.text = text
    article.image = image
    article.category_id = category_id

    article = await article_repository.update_article(
        session,
        article,
    )

    await publish_message(
        "article_embedding",
        {
            "article_id": article.id,
            "text": article.text,
        },
    )

    return article


async def get_articles(
        session: AsyncSession,
        search: str | None = None,
        category_id: int | None = None,
        page_number: int = 1,
        page_size: int = 10,
):
    return await article_repository.get_articles(
        session=session,
        search=search,
        category_id=category_id,
        page_number=page_number,
        page_size=page_size,
    )


async def delete_article(
        session: AsyncSession,
        article_id: int,
        user: User,
) -> Article:

    article = await article_repository.get_article(
        session,
        article_id)

    if not article or article.is_deleted:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    if user.role != "admin" and article.author_id != user.id:
        raise HTTPException(
            status_code=403,
        )

    article.is_deleted = True

    return await article_repository.delete_article(
        session,
        article,
    )
