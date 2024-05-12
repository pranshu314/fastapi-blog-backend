from typing import Optional, Any

from pydantic import BaseModel, field_validator, Field, EmailStr, StrictBool

from models.pyobjectid import PyObjectId


class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    disabled: StrictBool = False


class UserCreate(UserBase):
    password: str = Field(...)

    @field_validator("username")
    def validate_username(cls: Any, username: str, **kwargs: Any) -> Any:
        if len(username) <= 4:
            raise ValueError("Username is too short")
        return username

    @field_validator("email")
    def validate_email(cls: Any, email: str, **kwargs: Any) -> Any:
        if len(email) == 0:
            raise ValueError("Email is empty")
        return email


class User(UserBase):
    id: Optional[PyObjectId] = Field(None)

    class Config:
        from_attributes: bool = True


class UserInDB(User):
    hashed_password: str = Field(...)


class UserUpdate(UserBase):
    password: Optional[str] = Field(None)

    class Config:
        from_attributes: bool = True


class UserPassword(BaseModel):
    password: Optional[str] = Field(None)
