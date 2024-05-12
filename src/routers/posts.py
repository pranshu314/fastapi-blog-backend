from http import HTTPStatus
from typing import Any, Optional

from fastapi import Depends, HTTPException, status, APIRouter, Response

from models.pyobjectid import PyObjectId
import schemas
import services

router: Any = APIRouter(
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/posts",
    response_model=schemas.PostInDb,
    status_code=status.HTTP_201_CREATED,
)
def create_user_post(
    post: schemas.PostCreate,
    db: Any = Depends(services.get_db),
    current_user: schemas.User = Depends(services.get_current_user),
) -> Any:
    result = services.create_post(db=db, post=post, current_user=current_user)
    return result


@router.get("/post/{slug}", response_model=schemas.Posts)
def read_slug(slug: str, db: Any = Depends(services.get_db)) -> Any:
    db_slug = services.get_post(db=db, slug=slug)
    if db_slug is None:
        raise HTTPException(status_code=404, detail="Not found")
    return db_slug


@router.get("/posts", response_model=schemas.Posts)
def list_posts(
    response: Response,
    db: Any = Depends(services.get_db),
    user_id: Optional[PyObjectId] = None,
) -> Any:
    db_user = ""
    if user_id:
        db_user = services.get_user_by_id(db=db, user_id=user_id)
        if db_user:
            posts = services.get_posts_by_userid(db=db, userid=user_id)
    else:
        posts = services.get_all_posts(db=db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="Not found")

    total_posts = services.count_posts(db=db)
    response.headers["X-Total-Posts"] = str(total_posts)

    return posts


@router.put("/posts/{slug}", response_model=schemas.PostInDb)
def update_user_post(
    slug: str,
    post: schemas.PostCreate,
    db: Any = Depends(services.get_db),
    current_user: schemas.User = Depends(services.get_current_user),
) -> Any:
    post_data = services.get_post(db=db, slug=slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="Not found")
    elif post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    req_post = services.update_post(db=db, slug=slug, post=post)
    return req_post


@router.delete("/posts/{slug}")
def post_delete(
    slug: str,
    db: Any = Depends(services.get_db),
    current_user: schemas.User = Depends(services.get_current_user),
) -> Any:
    post_data = services.get_post(db=db, slug=slug)
    if post_data is None:
        raise HTTPException(status_code=404, detail="Not found")
    if post_data.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    services.delete_post(db=db, slug=slug)
    return Response(status_code=HTTPStatus.NO_CONTENT.value)
