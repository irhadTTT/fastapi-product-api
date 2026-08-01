from datetime import datetime, timedelta
from jose import jwt
from core.config import settings


def create_email_token(email: str):

    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )