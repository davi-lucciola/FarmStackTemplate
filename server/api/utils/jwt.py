from jose import jwt
from api.config import settings


def encode_token(payload: dict) -> str:
    return jwt.encode(payload, settings.TOKEN_SECRET, settings.ALGORITHM)


def decode_token(token: str):
    return jwt.decode(token, settings.TOKEN_SECRET, algorithms=[settings.ALGORITHM])
