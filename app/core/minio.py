import os
from dotenv import load_dotenv
from minio import Minio
from uuid import uuid4 as uuid

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "articles")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=os.getenv("MINIO_ROOT_USER"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
    secure=False,
)

def check_minio_connection() -> bool:
    return minio_client.bucket_exists("articles")

def upload_image(file, filename: str) -> str:

    object_name = f"{uuid()}_{filename}"

    minio_client.put_object(
        MINIO_BUCKET_NAME,
        object_name,
        file,
        length=-1,
        part_size=10 * 1024 * 1024,
    )
    return object_name