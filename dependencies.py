import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from database import get_db
from models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:
            raise UnauthorizedException("Invalid token")

    except JWTError:
        raise UnauthorizedException("Invalid token")

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise NotFoundException("User not found")

    return user


def get_current_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise BadRequestException("Admin privileges required")

    return current_user
