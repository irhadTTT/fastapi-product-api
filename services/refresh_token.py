from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from core.exception import NotFoundException, UnauthorizedException
from core.logging import logger
from core.security import create_refresh_token
from jwt_handler import create_access_token
from models.refresh_token import RefreshToken
from models.user import User
from repositories import refresh_token_repository
from services.cache_service import delete_cache_pattern, get_cache, set_cache


class RefreshTokenService:
    @staticmethod
    async def save_refresh_token(db: Session, user_id: int):
        token = create_refresh_token()

        if token is None:
            logger.warning("Token not created by user_id=%s", user_id)
            raise NotFoundException("User not found")

        db_refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=datetime.now(timezone.utc).replace(tzinfo=None)
            + timedelta(days=30),
        )

        token = refresh_token_repository.create(db, db_refresh_token)

        logger.info("Refresh token created token_id=%s", token.id)

        await delete_cache_pattern("refresh_token:*")

        logger.debug(
            "Refresh_token cache invalidated pattern=%s action=%s",
            "refresh_token:*",
            "save_refresh_token",
        )

        return token

    @staticmethod
    async def get_token(db: Session, token: str):

        cache_key = f"refresh_token:token:{token}"

        cached = await get_cache(cache_key)

        if cached:
            logger.debug("Refresh token fetched from cached_id=%s", cached["id"])
            return RefreshToken(
                id=cached["id"],
                token=cached["token"],
                user_id=cached["user_id"],
                expires_at=datetime.fromisoformat(cached["expires_at"]),
                revoked=cached["revoked"],
            )

        token = refresh_token_repository.get_by_token(db, token)

        if token is None:
            logger.warning("Refresh token not found")
            raise NotFoundException("Refresh token not found")

        logger.info("Refresh token fetched from database token_id=%s", token.id)

        await set_cache(
            cache_key,
            {
                "id": token.id,
                "token": token.token,
                "user_id": token.user_id,
                "expires_at": token.expires_at.isoformat(),
                "revoked": token.revoked,
            },
            expire=300,
        )

        logger.debug("Refresh token cache updated token_id=%s", token.id)

        return token

    @staticmethod
    async def refresh_access_token(token: str, db: Session):
        refresh_token = await RefreshTokenService.get_token(db, token)

        if refresh_token is None:
            logger.warning("Token not found token=%s", token)
            raise UnauthorizedException("Invalid refresh token")

        if refresh_token.revoked:
            logger.warning("Token revoked=%s", token)
            raise UnauthorizedException("Refresh token has been revoked")

        if refresh_token.expires_at < datetime.now(timezone.utc).replace(tzinfo=None):
            logger.warning("Token expired=%s", token)
            raise UnauthorizedException("Refresh token has expired")

        user = db.query(User).filter(User.id == refresh_token.user_id).first()

        if user is None:
            logger.warning("User not found")
            raise NotFoundException("User not found")

        access_token = create_access_token(
            data={"sub": str(refresh_token.user_id), "role": user.role}
        )

        logger.info(
            "Access token is successfully changed user_id=%s role=%s",
            user.id,
            user.role,
        )

        logger.debug(
            "refresh_token cache invalidated pattern=%s action=%s",
            "refresh_token:*",
            "refresh_access_token",
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
