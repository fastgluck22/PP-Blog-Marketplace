from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email:Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )
    password_hash:Mapped[str] = mapped_column(     # тут не пароль, а его ХЭШ!!!!!!!
        String(255),
        nullable=False,
    )

    role:Mapped[str] = mapped_column(
        String(30),
        default="user",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
    )