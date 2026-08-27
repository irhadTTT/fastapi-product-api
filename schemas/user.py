from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_verified: bool | None = None

    class Config:
        from_attributes = True


class UsersResponse(BaseModel):
    users: list[UserResponse]
    page: int
    limit: int
    total: int
    total_pages: int


class UserBasicResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
