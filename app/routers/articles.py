from fastapi import Depends, APIRouter, Query
from fastapi import File, Form, UploadFile
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.article import Article
from app.db.models.user import User
from app.schemas.article import ArticleResponse, ArticleUpdate
from app.core.minio import upload_image
from app.services import article_service

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)

@router.get("/", response_model=list[ArticleResponse])
async def get_articles(
        search: str | None = None,
        category_id: int | None = None,
        page_number: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1,le=100),
        session: AsyncSession = Depends(get_session),
):
    return await article_service.get_articles(
        session=session,
        search=search,
        category_id=category_id,
        page_number=page_number,
        page_size=page_size,
    )


@router.post("/", response_model=ArticleResponse)
async def create_article(
        request: Request,
        title: str = Form(...),
        text: str = Form(...),
        category_id: int = Form(...),
        image: UploadFile = File(...),
        session: AsyncSession = Depends(get_session),
):
    object_name = upload_image(
        image.file,
        image.filename or "image",
    )

    article = Article(
        title=title,
        text=text,
        image=object_name,
        category_id=category_id,
        author_id=request.state.user_id,
    )

    article = await article_service.create_article(
        session=session,
        article=article,
    )

    return article

@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
        article_id: int,
        request: Request,
        data: ArticleUpdate,
        session: AsyncSession = Depends(get_session),
):

    user = await session.get(
        User,
        request.state.user_id,
    )

    return await article_service.update_article(
        session=session,
        article_id=article_id,
        user=user,
        title=data.title,
        text=data.text,
        image=data.image,
        category_id=data.category_id,
    )


@router.delete("/{article_id}", response_model=ArticleResponse)
async def delete_article(
        article_id: int,
        request: Request,
        session: AsyncSession = Depends(get_session),
):

    user = await session.get(User, request.state.user_id)

    return await article_service.delete_article(
        session=session,
        article_id=article_id,
        user=user,
    )