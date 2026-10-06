from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category


async def create_category(
        session: AsyncSession,
        category: Category,
):
    session.add(category)
    await session.commit()
    await session.refresh(category)

    return category


async def get_categories(
        session: AsyncSession,
):
    result = await session.execute(
        select(Category)
    )

    return result.scalars().all()