import aio_pika

from app.config import settings


async def get_rabbitmq_connection():
    return await aio_pika.connect_robust(
        host=settings.rabbitmq_host,
        port=settings.rabbitmq_port,
        login=settings.rabbitmq_user,
        password=settings.rabbitmq_password,
    )