from datetime import timedelta
from os import walk
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

import schemas
import services
from models.pyobjectid import PyObjectId

router: Any = APIRouter(
    tags=["users"],
    responses={404: {"Description": "Not found"}},
)


@router.post(
    "/users",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create user",
)
def create_new_user(
    user: schemas.UserCreate,
    db: Any = Depends(services.get_db),
) -> Any:
    db_username = services.get_user_by_username(db=db, username=user.username)
    db_email = services.get_user_by_email(db=db, email=user.email)
    if db_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    elif db_email:
        raise HTTPException(status_code=400, detail="Email already taken")
    return services.create_user(db=db, user=user)


@router.get(
    "/users",
    response_model=schemas.User,
)
def list_users(db: Any = Depends(services.get_db)) -> List:
    users = services.get_users(db=db)
    return users


@router.get(
    "/users/user",
    response_model=schemas.User,
)
def read_user(
    username: Optional[str] = None,
    user_id: Optional[PyObjectId] = None,
    db: Any = Depends(services.get_db),
) -> Any:
    if username:
        db_user = services.get_user_by_username(db=db, username=username)
    elif user_id:
        db_user = services.get_user_by_id(db=db, user_id=user_id)
    else:
        raise HTTPException(status_code=404, detail="Not found")

    if db_user is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_user


@router.post(
    "/token",
    response_model=schemas.Token,
)
def login_for_access_token(
    db: Any = Depends(services.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    response: Response = None,
) -> Any:
    user = services.authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=services.security.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = services.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token_data = {"access_token": access_token, "token_type": "bearer"}
    response.set_cookie(
        key="token",
        value=access_token,
        max_age=access_token_expires.total_seconds(),
        httponly=True,
    )
    return token_data


@router.get(
    "/users/me/posts",
    response_model=schemas.Posts,
)
def read_own_posts(
    current_user: schemas.User = Depends(services.get_current_user),
    db: Any = Depends(services.get_db),
) -> List:
    user_id = current_user.id
    user_posts = services.get_posts_by_userid(db=db, userid=user_id)
    return user_posts


@router.put(
    "/users/{username}",
    response_model=schemas.User,
    response_model_exclude_none=True,
)
def update_user_prof(
    username: str,
    user: schemas.UserUpdate,
    current_user: schemas.User = Depends(services.get_current_user),
    db: Any = Depends(services.get_db),
) -> Any:
    if username != current_user.username:
        raise HTTPException(status_code=403, detail="Forbidden")

    result = services.update_user(db=db, user=user, username=username)
    return result
