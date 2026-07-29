from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from database import get_db
from sqlalchemy.orm import Session
from models import User
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()


    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )


    return user

def get_current_admin(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required"
        )

    return current_user