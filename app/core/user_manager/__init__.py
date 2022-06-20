import uuid
from typing import AsyncGenerator, Optional

from fastapi import Depends, Request
from fastapi_users import FastAPIUsers
from app.core.user_manager.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)

from app.api.deps import get_user_db
from app.core.config import settings
from app.db.tables import User
from app.core.user_manager.manager import SQLAlchemyUserDatabase, UserManager

async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator:
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


api_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = api_users.current_user(active=True)
current_active_super_user = api_users.current_user(active=True, superuser=True)
