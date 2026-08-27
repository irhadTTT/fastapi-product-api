from sqlalchemy.orm import Session

from core.exception import (
    BadRequestException,
    NotFoundException,
)
from core.logging import logger
from core.security import create_email_token
from core.worker.tasks import send_verification_email_task
from enums.sort import UserRole
from models.user import User
from repositories import user_repository
from schemas.auth import PasswordReset
from schemas.user import UserBasicResponse, UserCreate, UserResponse
from security import hash_password
from services.cache_service import delete_cache_pattern, get_cache, set_cache


class UserService:
    @staticmethod
    async def get_users(db: Session, current_user: User, page, limit):
        cache_key = f"users:list:{page}:{limit}"

        cached = await get_cache(cache_key)

        if cached:
            logger.debug(
                "Users fetched from cache page=%s limit=%s count=%s",
                page,
                limit,
                len(cached["users"]),
            )
            return {
                "users": [
                    UserResponse.model_validate(user) for user in cached["users"]
                ],
                "page": cached["page"],
                "limit": cached["limit"],
                "total": cached["total"],
                "total_pages": cached["total_pages"],
            }

        users, total = user_repository.get_all(db, page, limit)

        logger.info(
            "Users fatched from database page=%s limit=%s count=%s",
            page,
            limit,
            len(users),
        )

        response = [UserResponse.model_validate(user) for user in users]

        total_pages = (total + limit - 1) // limit

        result = {
            "users": response,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
        }

        await set_cache(
            cache_key,
            {
                "users": [user.model_dump(mode="json") for user in response],
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": total_pages,
            },
            expire=300,
        )

        logger.debug(
            "Users cache updated page=%s limit=%s count=%s", page, limit, len(response)
        )

        return result

    @staticmethod
    async def get_all_users(db: Session):
        users = user_repository.get_all_users(db)

        return [UserBasicResponse.model_validate(user) for user in users]

    @staticmethod
    async def create_user(user: UserCreate, db: Session, current_user: User):
        existing_user = user_repository.get_by_username(db, user.username)

        if existing_user:
            logger.warning("Username already exists for username=%s", user.username)
            raise BadRequestException("Username already exists")

        existing_email = user_repository.get_by_email(db, user.email)

        if existing_email:
            logger.warning("Email already exists for email=%s", user.email)
            raise BadRequestException("Email already exists")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
        )

        created_user = user_repository.create(db, new_user)

        token = create_email_token(created_user.email)

        send_verification_email_task.delay(created_user.email, token)

        logger.info(
            "User created user_id=%s username=%s email=%s created_by=%s",
            created_user.id,
            created_user.username,
            created_user.email,
            current_user.id,
        )

        await delete_cache_pattern("users:*")

        logger.debug("User cache invalidated pattern=%s action=%s", "users:*", "create")

        return created_user

    @staticmethod
    async def delete_user(user_id: int, db: Session, current_user: User):

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            logger.warning("User not found user_id=%s", user_id)
            raise NotFoundException("User not found")

        user_repository.delete(db, user)

        logger.info(
            "User deleted user_id=%s username=%s deleted_by=%s",
            user.id,
            user.username,
            current_user.id,
        )

        await delete_cache_pattern("users:*")

        logger.debug(
            "Users cache invalidated after deletion pattern=%s action=%s",
            "users:*",
            "delete",
        )

    @staticmethod
    async def change_role(user_id: int, role: str, db: Session, current_user: User):

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            logger.warning("User not found user_id=%s", user_id)
            raise NotFoundException("User not found")

        if role not in [UserRole.user, UserRole.admin]:
            logger.warning("Invalid role role=%s", role)
            raise BadRequestException("Invalid role")

        user.role = role
        user = user_repository.save(db, user)

        logger.info(
            "User role successfully changed user_id=%s role=%s changed_by=%s",
            user.id,
            user.role,
            current_user.id,
        )

        await delete_cache_pattern("users:*")

        logger.debug(
            "Users cache invalidated pattern=%s action=%s", "users:*", "change_role"
        )

        return {"message": "Role updated", "user": user.username, "role": user.role}

    @staticmethod
    def make_first_admin(user_id: int, db: Session):
        existing_admin = user_repository.get_admin(db)

        if existing_admin:
            logger.warning("Admin already exists user_id=%s", user_id)
            raise BadRequestException("Admin already exists")

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            logger.warning("User not found user_id=%s", user_id)
            raise NotFoundException("User not found")

        user.role = UserRole.admin
        user = user_repository.save(db, user)

        logger.info("Admin successfully created user_id=%s role=%s", user.id, user.role)

        delete_cache_pattern("users:*")

        logger.debug(
            "Users cache invalidated after deletion pattern=%s action=%s",
            "users:*",
            "make_first_admin",
        )

        return {
            "message": "First admin created",
            "username": user.username,
            "role": user.role,
        }

    @staticmethod
    def reset_password(
        user_id: int, data: PasswordReset, db: Session, current_user: User
    ):

        user = user_repository.get_by_id(db, user_id)

        if user is None:
            logger.warning("User not found user_id=%s", user_id)
            raise NotFoundException("User not found")

        user.password = hash_password(data.new_password)

        user = user_repository.save(db, user)

        logger.info("Password successfully reset user_id=%s", user.id)

        delete_cache_pattern("users:*")

        logger.debug(
            "Users cache invalidated after deletion pattern=%s action=%s",
            "users:*",
            "reset_password",
        )

        return {
            "message": "Password successfully changed",
            "username": user.username,
        }
