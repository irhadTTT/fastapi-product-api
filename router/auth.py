from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import LoginRequest
from database import get_db
from models import User
from security import verify_password
from jwt_handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    access_token = create_access_token(
        data={
            "sub": str(user.id)
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }