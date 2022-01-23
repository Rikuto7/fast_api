import os
from fastapi import HTTPException, status
from typing import Optional, Dict
from sqlalchemy.orm import Session
from uuid import UUID
from jose import jwt, JWTError

from app.api.models.models import User
from app.api.schemas import schemas
from app.api.func import auth as auth_func


SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')


def get_user(db: Session, user_id: Optional[UUID] = None, username: Optional[str] = None) -> Dict:
    try:
        if user_id:
            user = db.query(User).filter(User.uuid==user_id).first()
        else:
            user = db.query(User).filter(User.username==username).first()
    except BaseException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='ユーザーが存在しません')
    return user


def get_current_user(db: Session, token: str) -> Dict:
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


def create_user(request: schemas.UserOut, db: Session) -> Dict:
    user = User(
        username=request.username,
        email=request.email,
        password=auth_func.Hash.get_password_hash(password=request.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
