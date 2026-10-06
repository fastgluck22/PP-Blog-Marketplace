import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbitmq_connection


async def main():
    connection = await get_rabbitmq_connection()
    channel = await connection.channel()

    await channel.declare_queue(
        "article_embedding",
        durable=True,
    )

    message = {
        "article_id": 1,
        "text": "Кошки любят спать и играть.",
    }

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode("utf-8"),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            content_type="application/json",
        ),
        routing_key="article_embedding",
    )

    print("Article message published")

    await connection.close()


if __name__ == "__main__":
    asyncio.run(main())