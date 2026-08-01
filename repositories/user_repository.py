from sqlalchemy.orm import Session
from models.user import User
from enums.sort import UserRole

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(
    db: Session,
    user_id: int
):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

def get_by_username(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

def get_by_email(
    db: Session,
    email: str
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def get_admin(
    db: Session
):
    return (
        db.query(User)
        .filter(User.role == UserRole.admin)
        .first()
    )


def create(
    db: Session,
    user: User
):
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete(
    db: Session,
    user: User
):
    db.delete(user)
    db.commit()

def save(
    db: Session,
    user: User
):
    db.commit()
    db.refresh(user)

    return user