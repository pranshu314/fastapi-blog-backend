from datetime import datetime
from typing import Any

from slugify import slugify

import models
import schemas

# BUG: Use slug instead of title while search for and getting posts


def create_post(db: Any, post: schemas.PostCreate, current_user: schemas.User) -> Any:
    post_data = post.model_dump()
    post_data["slug"] = slugify(post_data["title"])
    user_data = schemas.User.from_orm(current_user).dict()
    post_data["author_id"] = user_data["id"]
    post_data["published_at"] = datetime.now()
    db_post = models.Post(**post_data)
    db.Posts.insert_one(db_post)
    return db_post


def get_post(db: Any, slug: str) -> Any:
    post = db.Posts.find_one({"slug": slug})
    return post


def get_all_posts(db: Any) -> list:
    posts = db.Posts.find().sort("published_at", -1)
    return posts


def get_posts_by_userid(db: Any, userid: models.pyobjectid.PyObjectId) -> list:
    return db.Posts.find({"author_id": userid})


def update_post(db: Any, post: Any, slug: str) -> Any:
    db_post = get_post(db, slug)
    post_data = post.dict()
    setattr(db_post, "body", post_data["body"])
    setattr(db_post, "slug", slugify(post_data["title"]))
    setattr(db_post, "summary", post_data["summary"])
    setattr(db_post, "title", post_data["title"])

    db.Posts.update_one({"slug": slug}, db_post)
    return db_post


def delete_post(db: Any, slug: str) -> Any:
    db.Posts.delete_one({"slug": slug})
    return None


def count_posts(db: Any) -> Any:
    total = db.Posts.count_documents({})
    return total
