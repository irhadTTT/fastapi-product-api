import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.exception import BadRequestException, NotFoundException, UnauthorizedException
from core.logging import logger
from core.security import create_email_token, verify_email_token
from core.worker.tasks import (
    send_password_reset_email_task,
    send_verification_email_task,
)
from jwt_handler import create_access_token
from models.user import User
from repositories import password_reset_repository, user_repository
from schemas.user import UserCreate
from security import hash_password, verify_password
from services.cache_service import delete_cache_pattern
from services.refresh_token import RefreshTokenService


class AuthService:
    @staticmethod
    async def login(
        request: Request, form_data: OAuth2PasswordRequestForm, db: Session
    ):
        user = user_repository.get_by_username(db, form_data.username)

        if user is None or not verify_password(form_data.password, user.password):
            logger.warning(
                "Failed login attempt for username=%s",
                form_data.username,
            )
            raise UnauthorizedException("Invalid username or password")

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        refresh_token = await RefreshTokenService.save_refresh_token(db, user.id)

        logger.info(
            "User logged in successfully user_id=%s username=%s",
            user.id,
            user.username,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token.token,
            "token_type": "bearer",
        }

    @staticmethod
    async def register(user: UserCreate, db: Session):
        existing_user = user_repository.get_by_email(db, user.email)

        if existing_user:
            logger.warning(
                "Registration attempt with existing email=%s",
                user.email,
            )
            raise BadRequestException("Email already registered.")

        existing_username = user_repository.get_by_username(db, user.username)

        if existing_username:
            logger.warning(
                "Registration attempt with existing email=%s",
                user.email,
            )
            raise BadRequestException("Username already exists.")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
        )

        user_repository.create(db, new_user)

        logger.info(
            "New user created user_id=%s username=%s",
            new_user.id,
            new_user.username,
        )

        token = create_email_token(new_user.email)

        send_verification_email_task.delay(new_user.email, token)

        logger.info(
            "Verification email task queued user_id=%s email=%s",
            new_user.id,
            new_user.email,
        )

        logger.debug(
            "Users cache invalidated pattern=%s action=%s", "users:*", "register"
        )

        await delete_cache_pattern("users:*")

        return {"message": "User created successfully."}

    @staticmethod
    async def verify_email(token: str, db: Session):
        email = verify_email_token(token)

        if not email:
            raise BadRequestException("Invalid or expired verification link.")

        user = user_repository.get_by_email(db, email)

        if not user:
            raise NotFoundException("User not found.")

        if user.is_verified:
            return {"message": "Email already verified."}

        user.is_verified = True

        db.commit()
        db.refresh(user)

        logger.info(
            "User email verified user_id=%s email=%s",
            user.id,
            user.email,
        )

        return {"message": "Email verified successfully."}

    @staticmethod
    async def forgot_password(email: str, db: Session):
        user = user_repository.get_by_email(db, email)

        if not user:
            raise NotFoundException("User not found.")

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(
            minutes=30
        )

        password_reset_repository.create(
            db=db,
            user_id=user.id,
            token=token,
            expires_at=expires_at,
        )

        send_password_reset_email_task.delay(
            user.email,
            token,
        )

        logger.info(
            "Password reset email task queued user_id=%s email=%s",
            user.id,
            user.email,
        )

        return {"message": "Password reset email sent."}

    @staticmethod
    async def reset_password(
        token: str,
        new_password: str,
        db: Session,
    ):
        reset_token = password_reset_repository.get_by_token(
            db,
            token,
        )

        if not reset_token:
            raise BadRequestException("Invalid or expired reset token.")

        if reset_token.used:
            raise BadRequestException("Reset token has already been used.")

        if reset_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            raise BadRequestException("Reset token has expired.")

        user = user_repository.get_by_id(
            db,
            reset_token.user_id,
        )

        if not user:
            raise NotFoundException("User not found.")

        user.password = hash_password(new_password)

        password_reset_repository.mark_as_used(
            db,
            reset_token,
        )

        db.commit()
        db.refresh(user)

        logger.info(
            "Password reset successfully user_id=%s",
            user.id,
        )

        return {"message": "Password reset successfully."}
