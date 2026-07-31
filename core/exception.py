from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

class NotFoundException(AppException):
    def __init__(self, detail="Resource not found"):
        super().__init__(404, detail)

class ForbiddenException(AppException):
    def __init__(self, detail="Forbidden"):
        super().__init__(403, detail)

class UnauthorizedException(AppException):
    def __init__(self, detail="Bad request"):
        super().__init__(401, detail)

class BadRequestException(AppException):
    def __init__(self, detail="Bad request"):
        super().__init__(400, detail)


async def app_exception_handler(
    request: Request,
    exc: AppException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail
        }
    )