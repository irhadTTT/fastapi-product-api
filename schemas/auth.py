from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str

class PasswordReset(BaseModel):
    new_password: str