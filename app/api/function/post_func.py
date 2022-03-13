from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from uuid import UUID

from api.models.models import Post
from api.schemas import schemas


def get_posts(db: Session) -> list:
    try:
        posts = db.query(Post).all()
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の取得に失敗しました')
    return posts


def get_post(db: Session, id: int) -> dict:
    try:
        post = db.query(Post).filter(Post.id == id)
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の取得に失敗しました')
    return post


def create_post(db: Session, request: schemas.PostIn, user_id: UUID) -> dict:
    try:
        post = Post(
            **jsonable_encoder(request),
            user_id=user_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の保存に失敗しました')
    return post


def update_post(db: Session, request: schemas.PostIn, user_id: UUID, post: Post):
    try:
        if post.first().user_id == user_id:
            post.update(jsonable_encoder(request))
            db.commit()
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の更新に失敗しました')
    return post
