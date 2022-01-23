from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4

from ..database import Base
from .base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    uuid = Column(UUIDType(binary=False),
                  primary_key=True,
                  default=uuid4)
    email = Column(String(128), nullable=False, index=True, unique=True)
    username = Column(String(128), nullable=False, index=True, unique=True)
    password = Column(String(128), nullable=False, index=True)
    refresh_token = Column(String(128), nullable=True, index=True)
    posts = relationship('Post', back_populates='user')


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    content = Column(String(128))
    user_id = Column(UUIDType(binary=False), ForeignKey('users.uuid'))
    user = relationship('User', back_populates='posts')
