from app.core.minio import minio_client

print("до")
print(minio_client.bucket_exists("articles"))
print("после")