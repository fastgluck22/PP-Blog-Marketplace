from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta

from app.config import settings

SECRET_KEY = settings.jwt_secret

ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

password_hasher = PasswordHash.recommended()


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])



