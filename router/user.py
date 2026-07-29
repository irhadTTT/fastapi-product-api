from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_current_admin
from database import get_db
from models import User
from schema import UserCreate, UserResponse, PasswordReset
from security import hash_password



router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    users = db.query(User).all()

    return users

#Users dodavanje korisnika
@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        return {"message": "User not found"}

    db.delete(user)
    db.commit()

    return {"message": "User deleted"}

@router.put("/{user_id}/role")
def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if role not in ["user", "admin"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    user.role = role

    db.commit()
    db.refresh(user)

    return {
        "message": "Role updated",
        "user": user.username,
        "role": user.role
    }


@router.post("/make-first-admin")
def make_first_admin(
    user_id: int,
    db: Session = Depends(get_db)
):

    existing_admin = db.query(User).filter(
        User.role == "admin"
    ).first()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Admin already exists"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.role = "admin"

    db.commit()
    db.refresh(user)

    return {
        "message": "First admin created",
        "username": user.username,
        "role": user.role
    }


@router.put("/{user_id}/reset-password")
def reset_password(
    user_id: int,
    data: PasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()


    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    user.password = hash_password(
        data.new_password
    )

    db.commit()

    return {
        "message": "Password successfully changed",
        "username": user.username,
    }