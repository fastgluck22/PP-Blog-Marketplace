from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.db.models.user import User
from app.schemas.user import UserRegister, UserLogin
from app.core.security import password_hasher, create_access_token
from app.rabbitmq.producer import publish_message

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register")
async def register_user(
        data: UserRegister,
        session: AsyncSession = Depends(get_session),
):
    existing_user = await session.scalar(
        select(User).where(User.email == data.email)
    )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=password_hasher.hash(data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    await publish_message(
        "registration_email",
        {"email": user.email},
    )

    return user


@router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response,
        session: AsyncSession = Depends(get_session),
):
    user = await session.scalar(
        select(User).where(User.email == data.email)
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not password_hasher.verify(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )

    return {"message": "Logged in successfully"}
