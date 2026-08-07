from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class PasswordReset(BaseModel):
    new_password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str
