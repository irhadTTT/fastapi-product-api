from datetime import datetime

from sqlalchemy.orm import Session

from models.password_reset_token import PasswordResetToken


def create(
    db: Session,
    user_id: int,
    token: str,
    expires_at: datetime,
):
    reset_token = PasswordResetToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
    )

    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)

    return reset_token


def get_by_token(db: Session, token: str):
    return (
        db.query(PasswordResetToken).filter(PasswordResetToken.token == token).first()
    )


def mark_as_used(db: Session, reset_token: PasswordResetToken):
    reset_token.used = True

    db.commit()
    db.refresh(reset_token)

    return reset_token
