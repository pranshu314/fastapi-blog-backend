import os
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from .users import get_user_by_username

ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_hash_password(password: str) -> Any:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: Any) -> Any:
    return pwd_context.verify(password, hashed_password)


def authenticate_user(db: Any, username: str, password: str) -> Any:
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> Any:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    secret = str(os.getenv("SECRET_KEY"))
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=ALGORITHM)
    return encoded_jwt
