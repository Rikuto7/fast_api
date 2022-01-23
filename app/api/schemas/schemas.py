from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostIn(BaseModel):
    title: str
    content: str



class UserOut(BaseModel):
    uuid: UUID
    email: str
    username: str
    created_at: datetime
    updated_at: datetime
    posts: List[PostOut]

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    email: str
    username: str
    password: str
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str
