import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbitmq_connection


async def publish_message(queue_name: str, message:dict):
    connection = await get_rabbitmq_connection()

    channel = await connection.channel()

    await channel.declare_queue(
        queue_name,
        durable=True,
    )

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode('utf-8'),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            content_type="application/json",
        ),
        routing_key=queue_name,
    )
    print("Message published")

    await connection.close()


if __name__ == "__main__":
    asyncio.run(publish_message(
        "registration_email",
        {"email": "testmail@example.com"},
        )
    )


