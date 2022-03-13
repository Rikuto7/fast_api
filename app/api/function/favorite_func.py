from uuid import UUID

from sqlalchemy.orm import Session

from api.models.models import Favorite


def get_favorite(db: Session, favorite_id: int):
    favorite = db.query(Favorite).filter(Favorite.id == favorite_id)
    return favorite


def create_favorite(db: Session, user_id: UUID, post_id: int):
    favorite = Favorite(
        user_id=user_id,
        post_id=post_id
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite
