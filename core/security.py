import secrets
from datetime import datetime, timedelta, timezone

from jose import jwt

from core.config import settings


def create_email_token(email: str):

    payload = {"sub": email, "exp": datetime.now(timezone.utc) + timedelta(hours=24)}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token():
    return secrets.token_urlsafe(64)
