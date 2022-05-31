# USER CRUD

import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from app.api.deps import get_async_db, get_user_db
from app.core.logger import logger
from app.core.user_manager import get_user_manager
from app.db.schemas import UserCreate

get_async_db_context = contextlib.asynccontextmanager(get_async_db)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(email: str, password: str, is_superuser: bool = False) -> None:
    try:
        async with get_async_db_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    logger.info(f"User created {user}")
    except UserAlreadyExists:
        logger.info(f"User {email} already exists")
