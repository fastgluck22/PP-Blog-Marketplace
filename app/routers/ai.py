from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.services.article_vsearch import search_articles
from app.services.ai_service import build_context
from app.services.llm_service import generate_answer


router = APIRouter(prefix="/ai", tags=["AI"])

class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_question(
    data:QuestionRequest,
    session: AsyncSession = Depends(get_session),
):
    results = await search_articles(
        data.question,
        session,
        limit=1,
    )

    print("\nRESULTS:")
    for article, distance in results:
        print(article.id, article.title, distance)

    context = build_context(results)

    print("\nCONTEXT:")
    print(context)

    answer = await generate_answer(
        data.question,
        context,
    )

    return {
        "answer": answer,
    }
