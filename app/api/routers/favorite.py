from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.models import models
from api.schemas import schemas
from api.function import user_func, post_func, favorite_func
from db.database import get_db
import dependencies

router = APIRouter()

@router.get('/{user_id}/posts')
def get_favorite_posts(user_id: UUID, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_user(db=db, user_id=user_id).first()
    return user.favorite_posts


@router.get('/{post_id}/users')
def get_favorite_users(post_id: int, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    post = post_func.get_post(db=db, id=post_id).first()
    return post.favorite_users


@router.post('/')
def create_favorite_post(request: schemas, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    favorite = favorite_func.create_favorite(user_id=user.uuid, post_id=request.post_id)
    return favorite


@router.delete('/{favorite_id}')
def delete_favorite_post(favorite_id: int, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    favorite = favorite_func.get_favorite(db=db, favorite_id=favorite_id)
    favorite.delete()
    db.commit()
    return favorite
