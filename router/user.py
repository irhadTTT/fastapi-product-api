from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
)
from database import get_db
from dependencies import get_current_admin
from enums.sort import UserRole
from models.user import User
from repositories import user_repository
from schemas.auth import PasswordReset
from schemas.user import UserBasicResponse, UserCreate, UserResponse, UsersResponse
from security import hash_password
from services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=UsersResponse)
async def get_users(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return await UserService.get_users(db, current_user, page, limit)


@router.get("/all", response_model=list[UserBasicResponse])
async def get_all_users(db: Session = Depends(get_db)):
    return await UserService.get_all_users(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return await UserService.create_user(user, db, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    await UserService.delete_user(user_id, db, current_user)


@router.put("/{user_id}/role")
async def change_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return await UserService.change_role(user_id, role, db, current_user)


@router.post("/make-first-admin")
def make_first_admin(user_id: int, db: Session = Depends(get_db)):
    return UserService.make_first_admin(user_id, db)


@router.put("/{user_id}/reset-password")
def reset_password(
    user_id: int,
    data: PasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return UserService.reset_password(user_id, data, db, current_user)
