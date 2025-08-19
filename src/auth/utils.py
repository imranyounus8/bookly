import jwt
import uuid
import logging

from src.config import Config

from passlib.context import CryptContext
from datetime import timedelta, datetime

passwd_context = CryptContext(schemes=["bcrypt"])


def generate_passwd_hash(password: str) -> str:
    passwd_hash = passwd_context.hash(password)
    return passwd_hash


def verify_passwd(password: str, password_hash: str) -> bool:
    return passwd_context.verify(password, password_hash)


def create_access_token(
    user_data: dict, expiry: timedelta = None, refresh: bool = False
):
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(
            seconds=Config.ACCESS_TOKEN_EXPIRY
        )
    )
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload, algorithm=Config.JWT_ALGORITHM, key=Config.JWT_SECRET
    )
    return token


def decode_token(token: str) -> str:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
