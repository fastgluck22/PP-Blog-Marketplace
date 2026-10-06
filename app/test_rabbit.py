import asyncio

from app.core.rabbitmq import get_rabbitmq_connection


async def main():
    connection = await get_rabbitmq_connection()

    print("RabbitMQ connection OK")

    await connection.close()


asyncio.run(main())