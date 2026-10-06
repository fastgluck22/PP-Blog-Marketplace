from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category
from app.db.models.user import User
from app.repositories import category_repository


async def create_category(
        session: AsyncSession,
        user_id: int,
        name: str,
):
    user = await session.get(User, user_id)

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
        )

    category = Category(name=name)

    return await category_repository.create_category(
        session=session,
        category=category,
    )


async def get_categories(
        session: AsyncSession,
):
    return await category_repository.get_categories(
        session=session,
    )