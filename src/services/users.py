from typing import Any

# from session import db
import models
import schemas

from models.pyobjectid import PyObjectId
from . import security


def get_user_by_email(db: Any, email: str) -> Any:
    return db.Users.find_one({"email": email})


def get_user_by_id(db: Any, user_id: PyObjectId) -> Any:
    return db.Users.find_one({"_id": user_id})


def get_user_by_username(db: Any, username: str) -> Any:
    return db.Users.find_one({"username": username})


def get_users(db: Any) -> list:
    users = list(db.Users.find())
    return users


def create_user(db: Any, user: schemas.UserCreate) -> Any:
    hashed_password = security.get_hash_password(password=user.password)
    user_data = user.model_dump()
    del user_data["password"]
    user_data["hashed_password"] = hashed_password
    user_post = models.User(**user_data)
    db.Users.insert_one(user_post)
    return user_post


def update_user(db: Any, user: Any, username: str):
    db_user = get_user_by_username(db, username)
    user_data = user.dict()
    new_password = user_data["password"]
    if new_password:
        password = security.get_hash_password(password=new_password)
        setattr(db_user, "hashed_password", password)
    setattr(db_user, "username", user_data["username"])
    setattr(db_user, "email", user_data["email"])
    setattr(db_user, "disabled", user_data["disabled"])

    db.Users.update_one({"username": username}, db_user)
    return db_user
