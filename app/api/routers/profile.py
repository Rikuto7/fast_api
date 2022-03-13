from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.schemas import schemas
from api.function import user_func
from api.function import profile_func
from db.database import get_db
import dependencies


router = APIRouter()


@router.get('/', response_model=schemas.ProfileOut)
def get_profile(db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    profile = profile_func.get_profile(db=db, user_id=user.uuid).first()
    return profile


@router.post('/', response_model=schemas.ProfileOut)
def create_profile(request: schemas.ProfileIn, db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    return profile_func.create_profile(db=db, request=request, user_id=user.uuid)


@router.put('/', response_model=schemas.ProfileOut)
def update_profile(request: schemas.ProfileIn,
                   db: Session = Depends(get_db),
                   token: str = Depends(dependencies.oauth2_scheme)
                   ):
    user = user_func.get_current_user(db=db, token=token).first()
    profile = profile_func.get_profile(db=db, user_id=user.uuid)
    return profile_func.update_profile(db=db, request=request, profile=profile)


@router.delete('/')
def delete_profile(db: Session = Depends(get_db), token: str = Depends(dependencies.oauth2_scheme)):
    user = user_func.get_current_user(db=db, token=token).first()
    profile = profile_func.get_profile(db=db, user_id=user.uuid)
    profile_func.delete_profile(db=db, profile=profile)
