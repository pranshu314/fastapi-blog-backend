from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from .pyobjectid import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(...)
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    diabled: bool = Field(...)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "username": "Jhon Doe",
                "email": "jd@example.com",
                "hashed_password": "secret",
                "diabled": False,
            }
        }
