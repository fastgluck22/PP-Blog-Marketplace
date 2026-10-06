from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
# engine = мост между Python и PostgreSQL
from app.config import settings


engine = create_async_engine(   # движок / возможность подключиться к БД
    settings.database_url,
    echo=True,
)

async_session = async_sessionmaker(   # рабочая сессия, в рамках которой выполняются запросы
    engine,
    expire_on_commit=False,   # expire - истекший
)

async def check_db_connection():
    async with engine.connect() as connection:
        result = await connection.execute(text("SELECT 1"))
        print(result.scalar())

async def get_session():
    async with async_session() as session:
        yield session