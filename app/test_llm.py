import asyncio

from app.services.llm_service import generate_answer


async def main():
    answer = await generate_answer(
        question="Как выбрать ноутбук для учебы?",
        context=(
            "Как выбрать ноутбук для учебы и работы. "
            "При выборе стоит учитывать процессор, "
            "оперативную память, SSD, автономность и вес."
        ),
    )

    print("\nОтвет:")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())