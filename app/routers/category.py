from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service


router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.post("/", response_model=CategoryResponse)
async def create_category(
        data: CategoryCreate,
        request: Request,
        session: AsyncSession = Depends(get_session),
):
    return await category_service.create_category(
        session=session,
        user_id=request.state.user_id,
        name=data.name,
    )


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
        session: AsyncSession = Depends(get_session),
):
    return await category_service.get_categories(
        session=session,
    )