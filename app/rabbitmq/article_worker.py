import asyncio
import json

import aio_pika

from app.core.embedding import create_embedding
from app.core.rabbitmq import get_rabbitmq_connection
from app.db.database import async_session
from app.db.models.article import Article


async def main():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()

    queue = await channel.declare_queue(
        "article_embedding",
        durable = True,
    )

    print("Waiting for messages")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode('utf-8'))

                article_id = data["article_id"]
                text = data["text"]

                embedding = create_embedding(text)

                async with async_session() as session:
                    article = await session.get(Article, article_id)

                    if article is None:
                        print(f"Article {article_id} not found")
                        continue

                    article.embedding = embedding

                    await session.commit()

                    print(f"Embedding saved for article {article_id}")

                print(f"Article ID: {article_id}")
                print(f"Embedding size: {len(embedding)}")

if __name__ == "__main__":
    asyncio.run(main())