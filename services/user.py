from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    NotFoundException,
)
from enums.sort import UserRole
from models.user import User
from repositories import user_repository
from schemas.auth import PasswordReset
from schemas.user import UserCreate
from security import hash_password


class UserService:

    @staticmethod
    def create_user(
        user: UserCreate,
        db: Session,
        current_user: User
    ):
        existing_user = user_repository.get_by_username(db, user.username)

        if existing_user:
            raise BadRequestException("Username already exists")
        
        existing_email = user_repository.get_by_email(db, user.email)
        
        if existing_email:
            raise BadRequestException("Email already exists")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password)
        )

        return user_repository.create(db, new_user)


    @staticmethod
    def delete_user(
        user_id: int,
        db: Session,
        current_user: User
    ):
        user = user_repository.get_by_id(db, user_id)

        if user is None:
            raise NotFoundException("User not found")

        user_repository.delete(db, user)


    @staticmethod
    def change_role(
        user_id: int,
        role: str,
        db: Session,
        current_user: User
    ):
        user = user_repository.get_by_id(db, user_id)

        if user is None:
            raise NotFoundException("User not found")

        if role not in [UserRole.user, UserRole.admin]:
            raise BadRequestException("Invalid role")

        user.role = role
        user = user_repository.save(db, user)

        return {
            "message": "Role updated",
            "user": user.username,
            "role": user.role
        }

    @staticmethod
    def make_first_admin(
        user_id: int,
        db: Session
    ):
        existing_admin = user_repository.get_admin(db)

        if existing_admin:
            raise BadRequestException("Admin already exists")

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            raise NotFoundException("User not found")

        user.role = UserRole.admin
        user = user_repository.save(db, user)

        return {
            "message": "First admin created",
            "username": user.username,
            "role": user.role
        }

    @staticmethod
    def reset_password(
        user_id: int,
        data: PasswordReset,
        db: Session,
        current_user: User
    ):

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            raise NotFoundException("User not found")

        user.password = hash_password(
            data.new_password
        )

        user = user_repository.save(db, user)

        return {
            "message": "Password successfully changed",
            "username": user.username,
        }