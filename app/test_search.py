import asyncio

from app.db.database import async_session
from app.services.article_vsearch import search_articles
from app.services.ai_service import build_context
from app.services.llm_service import generate_answer

async def main():
    question = "какой ноутбук выбрать для учебы?"

    async with async_session() as session:
        results = await search_articles(
            question,
            session,
        )

        context = build_context(results)

        answer = await generate_answer(
            question,
            context,
        )

        print("\nContext:")
        print(context)

        print("\nAnswer:")
        print(answer)


if __name__ == "__main__":
    asyncio.run(main())