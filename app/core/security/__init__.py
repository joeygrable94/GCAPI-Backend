import uuid
from typing import Any, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.config import settings
from app.core.security.authentication import (AuthenticationBackend,
                                              BearerTransport, JWTStrategy)
from app.core.security.authentication.authenticator import Authenticator
from app.core.security.manager import UserManager


async def get_user_manager(
    session: AsyncSession = Depends(get_async_db),
) -> AsyncGenerator:
    yield UserManager(session=session)


bearer_transport: BearerTransport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY, lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME
    )


auth_backend: AuthenticationBackend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,  # type: ignore
)

authenticator = Authenticator([auth_backend], get_user_manager)  # type: ignore

get_current_user_token: Any = authenticator.current_user_token(
    active=True, verified=settings.USERS_REQUIRE_VERIFICATION
)

get_current_active_user: Any = authenticator.current_user(
    active=True, verified=settings.USERS_REQUIRE_VERIFICATION
)

get_current_active_superuser = authenticator.current_user(
    active=True, verified=settings.USERS_REQUIRE_VERIFICATION, superuser=True
)
