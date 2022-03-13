from typing import Optional, Any
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.db.database import Base


class Token(BaseModel):
    access_token: str
    token_type: str


class EmailSchema(BaseModel):
    email: list[EmailStr]
    body: dict[str, Any]


class UserBase(BaseModel):
    uuid: UUID
    email: str
    username: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProfileBase(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ConnectionBase(BaseModel):
    id: int
    follower_id: UUID
    following_id: UUID

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    email: str
    username: str
    password: str


class UserOut(UserBase):
    posts: list[PostBase]
    profile: list[ProfileBase]

    class Config:
        orm_mode = True


class PostIn(BaseModel):
    title: str
    content: str


class PostOut(PostBase):
    user: UserBase

    class Config:
        orm_mode = True


class ProfileIn(BaseModel):
    content: str


class ProfileOut(ProfileBase):
    user: UserBase


class ConnectionIn(BaseModel):
    follower_id: UUID


class ConnectionOut(UserBase):
    pass

