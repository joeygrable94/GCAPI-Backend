from typing import AsyncGenerator, Optional, Tuple
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.errors import ErrorCode
from app.core.config import Settings, get_settings
from app.db.repositories import AccessTokensRepository, UsersRepository
from app.db.schemas import JWToken, UserRead
from app.db.tables import User

from .auth import (
    AuthException,
    AuthManager,
    BearerTransport,
    DatabaseStrategy,
    JWTStrategy,
)

bearer_transport: BearerTransport = BearerTransport(tokenUrl="auth/access")


async def get_jwt_strategy(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator:
    yield JWTStrategy(secret=settings.SECRET_KEY)


async def get_token_db(
    session: AsyncSession = Depends(get_async_db),
) -> AsyncGenerator[AccessTokensRepository, None]:
    token_repo: AccessTokensRepository = AccessTokensRepository(session)
    yield token_repo


async def get_user_db(
    session: AsyncSession = Depends(get_async_db),
) -> AsyncGenerator[UsersRepository, None]:
    user_repo: UsersRepository = UsersRepository(session)
    yield user_repo


async def get_db_strategy(
    token_db: AccessTokensRepository = Depends(get_token_db),
) -> AsyncGenerator:
    yield DatabaseStrategy(token_db=token_db)


async def get_user_auth(
    jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
    db_strategy: DatabaseStrategy = Depends(get_db_strategy),
    user_database: UsersRepository = Depends(get_user_db),
) -> AsyncGenerator:
    yield AuthManager(
        bearer=bearer_transport,
        jwt=jwt_strategy,
        tokens=db_strategy,
        user_db=user_database,
    )


async def get_current_user_access_token(
    settings: Settings = Depends(get_settings),
    token: str = Depends(bearer_transport.scheme),
    oauth: AuthManager = Depends(get_user_auth),
) -> Tuple[Optional[UserRead], Optional[str], Optional[JWToken]]:
    try:
        user_id: Optional[UUID]
        access_token: Optional[str]
        token_data: Optional[JWToken]
        user_id, access_token, token_data = await oauth.verify_token(
            token=token,
            audience=[settings.ACCESS_TOKEN_AUDIENCE],
            is_type="access",
            require_fresh=True,
        )
        if not user_id or not access_token or not token_data:
            return None, None, None
        current_user: Optional[User] = await oauth.users.read(entry_id=user_id)
        return UserRead.from_orm(current_user), access_token, token_data
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": status.HTTP_401_UNAUTHORIZED,
                "reason": e.reason,
            },
        )


async def get_current_verified_user(
    current_user_access_token: Tuple[
        Optional[UserRead], Optional[str], Optional[JWToken]
    ] = Depends(get_current_user_access_token),
) -> UserRead:
    current_user: Optional[UserRead]
    access_token: Optional[str]
    token_data: Optional[JWToken]
    current_user, access_token, token_data = current_user_access_token
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_NOT_FOUND
        )
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_VERIFIED,
        )
    return current_user


async def get_current_active_user(
    current_user: UserRead = Depends(get_current_verified_user),
) -> UserRead:
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=ErrorCode.USER_NOT_FOUND
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    return current_user


__all__ = [
    "AuthManager",
    "BearerTransport",
    "bearer_transport",
    "DatabaseStrategy",
    "JWTStrategy",
    "get_current_active_user",
    "get_current_user_access_token",
    "get_current_verified_user",
    "get_jwt_strategy",
    "get_token_db",
    "get_database_strategy",
    "get_user_auth",
]
