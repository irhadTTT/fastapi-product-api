from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.refresh_token import RefreshTokenRequest, RefreshTokenResponse
from services.refresh_token import RefreshTokenService

router = APIRouter(prefix="/refresh-access-token", tags=["Refresh-access-token"])


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate new access token using refresh token",
    status_code=status.HTTP_201_CREATED,
)
async def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return await RefreshTokenService.refresh_access_token(data.refresh_token, db)
