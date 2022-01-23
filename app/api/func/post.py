from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from uuid import UUID

from app.api.models.models import Post
from app.api.schemas import schemas


def get_posts(db: Session) -> List:
    try:
        posts = db.query(Post).all() 
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の取得に失敗しました')
    return posts


def get_post(db: Session, id: int) -> Dict:
    try:
        post = db.query(Post).filter(id==id).first()
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の取得に失敗しました')
    return post


def create_post(db: Session, request: schemas.PostIn, user_id: int) -> Dict:
    try:
        print(user_id)
        post = Post(
            title = request.title,
            content = request.content,
            user_id = user_id
        )
        db.add(post)
        db.commit()
        db.refresh(post)
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の保存に失敗しました')
    return post


def update_post(db: Session, request: schemas.PostIn, user_id: UUID, id: int):
    try:
        post = get_post(db=db, id=id)
        if post.user_id == user_id:
            post.title = request.title
            post.content = request.content
            db.commit()
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='投稿の更新に失敗しました')
    return post
