from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, Table
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType
from uuid import uuid4

from db.database import Base
from .base import TimestampMixin


connections = Table(
    'connections', Base.metadata,
    Column('following_id', UUIDType(binary=False),
           ForeignKey('users.uuid'), primary_key=True),
    Column('follower_id', UUIDType(binary=False),
           ForeignKey('users.uuid'), primary_key=True),
    UniqueConstraint('following_id', 'follower_id', name='unique_connection'),
)


class User(Base, TimestampMixin):
    __tablename__ = 'users'

    uuid = Column(UUIDType(binary=False),
                  primary_key=True,
                  default=uuid4)
    email = Column(String(128), nullable=False, index=True, unique=True)
    username = Column(String(128), nullable=False, index=True, unique=True)
    password = Column(String(128), nullable=False, index=True)
    refresh_token = Column(String(128), nullable=True, index=True)

    posts = relationship('Post', uselist=True)
    profile = relationship('Profile')
    following = relationship(
        'User', secondary=connections, uselist=True,
        primaryjoin=('connections.c.follower_id == User.uuid'),
        secondaryjoin=('connections.c.following_id == User.uuid'),
        backref=backref('follower', lazy='dynamic'), lazy='dynamic')
    favorite_posts = relationship('Post', secondary='favorites', uselist=True)

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def un_follow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            connections.c.following_id == user.uuid).count() > 0


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(128))
    user_id = Column(UUIDType(binary=False),
                     ForeignKey('users.uuid'), unique=True)

    user = relationship('User')


class Post(Base, TimestampMixin):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128))
    content = Column(String(128))
    user_id = Column(UUIDType(binary=False), ForeignKey('users.uuid'))

    user = relationship('User')
    favorite_users = relationship('User', secondary='favorites', uselist=True)


# class Connection(Base, TimestampMixin):
#     __tablename__ = 'connections'
#     __table_args__ = (UniqueConstraint('following_id','follower_id'),{})

#     id = Column(Integer, primary_key=True, index=True)
#     following_id = Column(UUIDType(binary=False), ForeignKey('users.uuid'))
#     follower_id = Column(UUIDType(binary=False), ForeignKey('users.uuid'))

#     following = relationship('User', foreign_keys=[following_id])
#     follower = relationship('User', foreign_keys=[follower_id])


class Favorite(Base, TimestampMixin):
    __tablename__ = 'favorites'
    __table_args__ = (UniqueConstraint('user_id', 'post_id'), {})

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUIDType(binary=False), ForeignKey('users.uuid'))
    post_id = Column(Integer, ForeignKey('posts.id'))
