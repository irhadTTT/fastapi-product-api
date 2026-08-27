import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from core.config import settings


def create_email_token(email: str):

    payload = {"sub": email, "exp": datetime.now(timezone.utc) + timedelta(hours=24)}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token():
    return secrets.token_urlsafe(64)


def verify_email_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        email = payload.get("sub")

        if not email:
            return None

        return email

    except JWTError:
        return None
