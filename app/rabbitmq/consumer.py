import asyncio
import json

import aio_pika

from app.core.rabbitmq import get_rabbitmq_connection
from app.email.sender import MockEmailSender



async def main():
    connection = await get_rabbitmq_connection()

    channel = await connection.channel()

    queue = await channel.declare_queue(
        "registration_email",
        durable=True
    )

    email_sender = MockEmailSender()

    print("Waiting for messages")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                data = json.loads(message.body.decode("utf-8"))

                await email_sender.send_registration_email(
                    data["email"],
                )


if __name__ == "__main__":
    asyncio.run(main())