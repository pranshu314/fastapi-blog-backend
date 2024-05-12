import os
from typing import Any

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

import schemas
from db.session import client

from .security import ALGORITHM, oauth2_scheme
from .users import get_user_by_username


def get_db():
    db = client.blog
    yield db


def get_current_user(db: Any, token: str = Depends(oauth2_scheme)) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        secret = os.getenv("SECRET_KEY")
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])

        username: Any = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise credentials_exception

    if token_data.username is None:
        raise credentials_exception
    user = get_user_by_username(db=db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> Any:
    if current_user.disabled:
        raise HTTPException(status_code=401, detail="Inactive user")
    return current_user
