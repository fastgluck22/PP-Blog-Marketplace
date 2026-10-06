from fastapi import FastAPI

from app.config import settings
from app.db.database import check_db_connection
from app.routers.articles import router as articles_router
from app.routers.category import router as categories_router
from app.routers.auth import router as auth_router
from app.middleware.auth import auth_middleware
from app.routers.ai import router as ai_router

app = FastAPI(
    title=settings.app_name,
)

@app.get("/health")
def health():
    return {"status": "ok"}

app.middleware("http")(auth_middleware)

app.include_router(categories_router, prefix="/api")
app.include_router(articles_router, prefix="/api")

app.include_router(auth_router, prefix="/api")

app.include_router(ai_router)
