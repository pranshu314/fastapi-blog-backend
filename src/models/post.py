from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field

from .pyobjectid import PyObjectId


class Post(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    slug: str = Field(...)
    title: str = Field(...)
    summary: str = Field(...)
    body: str = Field(...)
    published_at: datetime = Field(default=datetime.now())
    author_id: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Title",
                "sumary": None,
                "body": "Body",
                "published_at": datetime.now(),
                "author_id": "Id of author",
            }
        }
