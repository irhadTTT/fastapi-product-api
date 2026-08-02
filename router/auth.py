from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

from core.email import send_verification_email
from core.exception import BadRequestException, UnauthorizedException
from core.security import create_email_token
from database import get_db
from dependencies import get_current_user
from jwt_handler import create_access_token
from limiter import limiter
from models.user import User
from repositories import user_repository
from schemas.user import UserCreate, UserResponse
from security import hash_password, verify_password
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/login",
    summary="User login",
    description="Authenticate user and return JWT access token",
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    return await AuthService.login(request, form_data, db)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register user",
    description="Register new user",
)
def register(
    user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)
):
    return AuthService.register(user, background_tasks, db)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
