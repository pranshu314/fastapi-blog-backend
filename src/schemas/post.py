from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from models.pyobjectid import PyObjectId


class PostBase(BaseModel):
    title: str = Field(...)
    body: str = Field(...)
    summary: str = Field(...)


class PostCreate(PostBase):
    @field_validator("title")
    def validate_title(cls: Any, title: str, **kwargs: Any) -> Any:
        if len(title) == 0:
            raise ValueError("Title is empty")
        elif len(title) > 100:
            raise ValueError("Title is too long")
        return title

    @field_validator("summary")
    def validate_summary(cls: Any, summary: str, **kwargs: Any) -> Any:
        if len(summary) > 200:
            raise ValueError("Summary is too long")
        return summary

    @field_validator("body")
    def validate_body(cls: Any, body: str, **kwargs: Any):
        if len(body) == 0:
            raise ValueError("Body is empty")
        return body


class PostInDb(PostBase):
    title: str = Field(...)
    body: str = Field(...)
    summary: str = Field(...)
    id: Optional[PyObjectId] = Field(None)
    published_at: Optional[datetime] = Field(None)
    author_id: Optional[str] = Field(None)

    class Config:
        orm_model: bool = True


class Posts(PostInDb):
    pass


class PostUpdate(PostBase):
    author_id: str = Field(...)
