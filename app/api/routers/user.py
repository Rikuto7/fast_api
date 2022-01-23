import csv
from collections import namedtuple

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.database import get_db
from app.api.models.models import User
from app.api.func import user as user_func, auth as auth_func
from app.api.schemas import schemas


router = APIRouter()


@router.post('/login/', response_model=schemas.Token)
async def authenticate(db: Session = Depends(get_db), request: OAuth2PasswordRequestForm = Depends()):
    user = user_func.get_user(db=db, username=request.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="ユーザーが存在しません")
    if not auth_func.Hash.verify_password(plain_password=request.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='パスワードが正しくありません'
        )
    access_token = auth_func.create_access_token(data={'username': user.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
    }


@router.post('/register/', response_model=schemas.UserOut)
def create_user(request: schemas.UserIn, db: Session = Depends(get_db)):
    return user_func.create_user(db=db, request=request)


@router.get("/me/", response_model=schemas.UserOut)
async def read_users_me(db: Session = Depends(get_db), token: str = Depends(auth_func.oauth2_scheme)):
    return user_func.get_current_user(db, token)


@router.get("/{uuid}/", response_model=schemas.UserOut)
async def read_users_me(uuid: UUID, db: Session = Depends(get_db), token: str = Depends(auth_func.oauth2_scheme)):
    return user_func.get_user(db, user_id=uuid)


@router.get("/csv/")
async def export_csv(limit: Optional[int]=1000, db: Session = Depends(get_db)):
    file_path = "user.csv"
    category = ("uuid", "user_name", "email")
    submission = namedtuple("User_Export", category)
    user_list = db.query(User).limit(limit).all()
    data = []
    for user in user_list:
        value_list = []
        value_list.append(user.uuid)
        value_list.append(user.username)
        value_list.append(user.email)
        data.append(value_list)
    with open(file_path, "w", newline="", encoding="utf8") as f:
            writer = csv.writer(f)
            writer.writerow(submission._fields)
            writer.writerows(data)

    return FileResponse(path=file_path,filename="user.csv")
