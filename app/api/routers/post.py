from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
from sqlalchemy.orm import Session


from app.api.database import get_db
from app.api.models.models import User
from app.api.func import post as post_func, user as user_func
from app.api.schemas import schemas


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login/")

@router.get('/', response_model=List[schemas.PostOut])
async def get_post(db: Session = Depends(get_db)):
    posts = post_func.get_posts(db=db)
    return posts


@router.get('/{id}/', response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = post_func.get_post(db=db, id=id)
    return post


@router.post('/', response_model=schemas.PostOut)
async def get_post(request: schemas.PostIn, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = user_func.get_current_user(db=db, token=token)
    post = post_func.create_post(request=request, db=db, user_id=current_user.uuid)
    return post


@router.put('/{id}/', response_model=schemas.PostOut)
async def update_post(request: schemas.PostIn, id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = user_func.get_current_user(db=db, token=token)
    post = post_func.update_post(request=request, db=db, user_id=current_user.uuid, id=id)
    return post
