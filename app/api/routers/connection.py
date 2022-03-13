from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import dependencies
from db.database import get_db
from api.models import models
from api.schemas import schemas
from api.function import user_func


router = APIRouter()


@router.get('/followings', response_model=list[schemas.UserOut])
def get_followings(db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    followings = user.following.all()
    return followings


@router.get('/followers', response_model=list[schemas.UserOut])
def get_follower(db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    followers = user.follower.all()
    return followers


@router.post('/', response_model=schemas.ConnectionOut)
def create_connections(request: schemas.ConnectionIn, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    following = user_func.get_current_user(db=db, token=token).first()
    follower = user_func.get_user(db=db, user_id=request.follower_id).first()
    following.follow(follower)
    db.add(following)
    db.commit()
    return follower


@router.delete('/')
def delete_connections(request: schemas.ConnectionIn, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    following = user_func.get_current_user(db=db, token=token).first()
    follower = user_func.get_user(db=db, user_id=request.follower_id).first()
    following.un_follow(follower)
    db.add(following)
    db.commit()
    return follower
