from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from fastapi.encoders import jsonable_encoder

from api.schemas import schemas
from api.models.models import Profile


def get_profile(db: Session, user_id: UUID):
    profile = db.query(Profile).filter(
        Profile.user_id == user_id)
    return profile


def create_profile(db: Session, request: schemas.ProfileIn, user_id: UUID):
    try:
        profile = Profile(
            **jsonable_encoder(request),
            user_id=user_id
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    except BaseException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='プロフィールの作成に失敗しました')
    return profile


def update_profile(db: Session, request: schemas.ProfileIn, profile: Profile):
    try:
        profile.update(jsonable_encoder(request))
        db.commit()
    except BaseException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='プロフィールの更新に失敗しました')
    return profile.first()


def delete_profile(db: Session, profile: Profile):
    profile.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
