from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_pagination import Page, paginate

from db.database import get_db
from api.function import post_func, user_func
from api.schemas import schemas
import dependencies


router = APIRouter()


@router.get('/', response_model=Page[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db)):
    posts = post_func.get_posts(db=db)
    return paginate(posts)


@router.get('/{id}/', response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = post_func.get_post(db=db, id=id).first()
    return post


@router.post('/', response_model=schemas.PostOut)
async def create_post(request: schemas.PostIn, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    current_user = user_func.get_current_user(db=db, token=token).first()
    post = post_func.create_post(
        request=request, db=db, user_id=current_user.uuid)
    return post


@router.put('/{id}/', response_model=schemas.PostOut)
async def update_post(request: schemas.PostIn, id: int, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    current_user = user_func.get_current_user(db=db, token=token).first()
    post = post_func.get_post(db=db, id=id)
    return post_func.update_post(request=request, db=db, user_id=current_user.uuid, post=post).first()
