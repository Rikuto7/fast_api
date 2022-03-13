import os
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import Optional
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from api.models.models import User
from api.schemas import schemas
from api.function import auth_func


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


def get_user(db: Session, user_id: Optional[UUID] = None, username: Optional[str] = None) -> dict:
    try:
        if user_id:
            user = db.query(User).filter(User.uuid == user_id)
        else:
            user = db.query(User).filter(
                User.username == username)
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ユーザーが存在しません')
    return user


def get_current_user(db: Session, token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を確認できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def create_user(request: schemas.UserIn, db: Session) -> dict:
    try:
        user = User(
            username=request.username,
            email=request.email,
            password=auth_func.Hash.get_password_hash(
                password=request.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ユーザーの作成に失敗しました')
    return user


def update_user(request: schemas.UserIn, db: Session, user: User) -> dict:
    try:
        user.update(jsonable_encoder(request))
        db.commit()
    except BaseException as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
                            detail='ユーザーの更新に失敗しました')
    return user
