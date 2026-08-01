from fastapi import APIRouter, Depends, status, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from jwt_handler import create_access_token
from models.user import User
from schemas.user import UserCreate, UserResponse
from security import hash_password, verify_password
from dependencies import get_current_user
from limiter import limiter
from slowapi.util import get_remote_address
from core.exception import (
    BadRequestException,
    UnauthorizedException
)
from repositories import user_repository
from core.email import send_verification_email
from core.security import create_email_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return JWT access token"
    )
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = user_repository.get_by_username(db, form_data.username)

    if user is None or not verify_password(form_data.password, user.password):
        raise UnauthorizedException("Invalid username or password")

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
        "/register", 
        status_code=status.HTTP_201_CREATED,
        summary="Register user",
        description="Register new user",
    )
def register(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = user_repository.get_by_email(db, user.email)

    if existing_user:
        raise BadRequestException("Email already registered.")

    existing_username = user_repository.get_by_username(db, user.username)

    if existing_username:
        raise BadRequestException("Username already exists.")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    user_repository.create(db, new_user)

    token = create_email_token(
        new_user.email
    )

    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        token
    )

    return {
        "message": "User created successfully."
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user