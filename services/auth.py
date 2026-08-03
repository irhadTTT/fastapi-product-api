from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.exception import BadRequestException, UnauthorizedException
from core.security import create_email_token
from core.worker.tasks import send_verification_email_task
from jwt_handler import create_access_token
from models.user import User
from repositories import user_repository
from schemas.user import UserCreate
from security import hash_password, verify_password
from services.cache_service import delete_cache_pattern


class AuthService:
    @staticmethod
    async def login(
        request: Request, form_data: OAuth2PasswordRequestForm, db: Session
    ):
        user = user_repository.get_by_username(db, form_data.username)

        if user is None or not verify_password(form_data.password, user.password):
            raise UnauthorizedException("Invalid username or password")

        access_token = create_access_token(
            data={"sub": str(user.id), "role": user.role}
        )

        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def register(user: UserCreate, db: Session):
        existing_user = user_repository.get_by_email(db, user.email)

        if existing_user:
            raise BadRequestException("Email already registered.")

        existing_username = user_repository.get_by_username(db, user.username)

        if existing_username:
            raise BadRequestException("Username already exists.")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
        )

        user_repository.create(db, new_user)

        token = create_email_token(new_user.email)

        send_verification_email_task.delay(new_user.email, token)
        await delete_cache_pattern("users:*")

        return {"message": "User created successfully."}
