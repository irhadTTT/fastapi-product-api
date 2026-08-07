from sqlalchemy.orm import Session

from models.refresh_token import RefreshToken


def get_by_token(db: Session, token: str):
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def create(db: Session, refresh_token: RefreshToken):
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token
