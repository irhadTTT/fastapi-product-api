from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_admin
from enums.sort import UserRole
from models.user import User
from schemas.auth import PasswordReset
from schemas.user import UserCreate, UserResponse
from security import hash_password
from core.exception import (
    NotFoundException,
    ForbiddenException,
    BadRequestException,
)

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
@router.post(
    "/", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        raise BadRequestException("Username already exists")
    
    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        raise BadRequestException("Email already exists")
        
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise NotFoundException("User not found")

    db.delete(user)
    db.commit()


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
        raise NotFoundException("User not found")

    if role not in [UserRole.user, UserRole.admin]:
        raise BadRequestException("Invalid role")

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
        User.role == UserRole.admin
    ).first()

    if existing_admin:
        raise BadRequestException("Admin already exists")

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise NotFoundException("User not found")

    user.role = UserRole.admin

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
         raise NotFoundException("User not found")

    user.password = hash_password(
        data.new_password
    )

    db.commit()

    return {
        "message": "Password successfully changed",
        "username": user.username,
    }