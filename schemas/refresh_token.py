from datetime import datetime

from pydantic import BaseModel


class RefreshTokenCreate(BaseModel):
    token: str
    user_id: int
    expires_at: datetime


class RefreshTokenResponse(BaseModel):
    id: int
    token: str
    user_id: int
    expires_at: datetime
    revoked: bool

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
