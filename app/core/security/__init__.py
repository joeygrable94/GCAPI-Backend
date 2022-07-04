import uuid
from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings

from app.core.security.authentication import (AuthenticationBackend,
                                              BearerTransport,
                                              JWTStrategy)
from app.core.security.authentication.authenticator import Authenticator
from app.core.security.manager import UserManager
from app.db.tables import User
from app.db.user_db import SQLAlchemyUserDatabase
from app.api.deps import get_async_db


async def get_user_db(session: AsyncSession = Depends(get_async_db)) -> AsyncGenerator:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator:
    yield UserManager(user_db)

bearer_transport: BearerTransport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME
    )

auth_backend: AuthenticationBackend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

authenticator = Authenticator([auth_backend], get_user_manager)

def get_current_active_user() -> Any:
    return authenticator.current_user(
        active=True, verified=settings.USERS_REQUIRE_VERIFICATION
    )

def get_current_active_superuser() -> Any:
    return authenticator.current_user(
        active=True, verified=settings.USERS_REQUIRE_VERIFICATION, superuser=True
    )
