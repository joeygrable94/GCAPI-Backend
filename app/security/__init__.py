from typing import Any, AsyncGenerator, List, Literal, Optional, Tuple, Union
from uuid import UUID

from fastapi import Body, Depends, HTTPException, status
from fastapi_permissions import Authenticated, Everyone, configure_permissions
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.errors import ErrorCode
from app.api.exceptions import InvalidID, UserNotExists
from app.core.config import Settings, get_settings, settings
from app.core.utilities import parse_id
from app.db.repositories import AccessTokenRepository, UserRepository
from app.db.schemas import JWToken, UserRead
from app.db.schemas.user import UserPrincipals
from app.db.tables import User

from .auth import (
    AuthException,
    AuthManager,
    BearerTransport,
    DatabaseStrategy,
    JWTStrategy,
)

bearer_transport: BearerTransport = BearerTransport(
    tokenUrl="auth/access", tokenScopes=settings.BASE_PRINCIPALS
)


async def get_jwt_strategy(
    settings: Settings = Depends(get_settings),
) -> AsyncGenerator:  # pragma: no cover
    yield JWTStrategy(secret=settings.SECRET_KEY)


async def get_token_db(
    session: AsyncSession = Depends(get_async_db),
) -> AsyncGenerator[AccessTokenRepository, None]:  # pragma: no cover
    token_repo: AccessTokenRepository = AccessTokenRepository(session)
    yield token_repo


async def get_user_db(
    session: AsyncSession = Depends(get_async_db),
) -> AsyncGenerator[UserRepository, None]:  # pragma: no cover
    user_repo: UserRepository = UserRepository(session)
    yield user_repo


async def get_db_strategy(
    token_db: AccessTokenRepository = Depends(get_token_db),
) -> AsyncGenerator:  # pragma: no cover
    yield DatabaseStrategy(token_db=token_db)


async def get_user_auth(
    jwt_strategy: JWTStrategy = Depends(get_jwt_strategy),
    db_strategy: DatabaseStrategy = Depends(get_db_strategy),
    user_database: UserRepository = Depends(get_user_db),
) -> AsyncGenerator:  # pragma: no cover
    yield AuthManager(
        bearer=bearer_transport,
        jwt=jwt_strategy,
        tokens=db_strategy,
        user_db=user_database,
    )


# FETCH USERS
async def get_user_or_404(
    id: Any,
    oauth: AuthManager = Depends(get_user_auth),
) -> User:  # pragma: no cover
    """Parses uuid/int and fetches user by id."""
    try:
        parsed_id: UUID = parse_id(id)
        user: Optional[User] = await oauth.users.read(entry_id=parsed_id)
        if not user:
            raise UserNotExists()
        return user
    except (UserNotExists, InvalidID):  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )


async def get_current_user_by_email(
    email: EmailStr = Body(..., embed=True),
    oauth: AuthManager = Depends(get_user_auth),
) -> UserPrincipals:  # pragma: no cover
    """Fetches user by email string."""
    user: Optional[UserPrincipals] = await oauth.fetch_user(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    return UserPrincipals.from_orm(user)


# VERIFY/CONFIRM
async def get_current_user_for_verification(
    token: str,
    csrf: str,
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> User:
    try:
        user: UserPrincipals
        token_data: JWToken
        token_str: str
        # verify the token's associated user
        user, token_data, token_str = await oauth.verify_token(
            token=token,
            audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
            check_csrf=True,
            token_csrf=csrf,
        )
        db_user: Optional[User] = await oauth.users.read_by_email(
            email=user.email
        )  # pragma: no cover
        if not db_user:  # pragma: no cover
            raise UserNotExists()
        return db_user  # pragma: no cover
    except UserNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": status.HTTP_401_UNAUTHORIZED,
                "reason": e.reason,
            },
        )


# REFRESH
async def get_current_user_refresh_token(
    token: str = Depends(bearer_transport.scheme),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Tuple[UserPrincipals, JWToken, str]:  # pragma: no cover
    try:
        return await oauth.verify_token(
            token=token,
            audience=[settings.REFRESH_TOKEN_AUDIENCE],
            is_type="refresh",
        )
    except AuthException as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": status.HTTP_401_UNAUTHORIZED,
                "reason": e.reason,
            },
        )


async def get_current_verified_refresh_user(
    current_user_access_token: Tuple[UserPrincipals, JWToken, str] = Depends(
        get_current_user_refresh_token
    ),
) -> Tuple[UserPrincipals, JWToken, str]:  # pragma: no cover
    current_user: UserPrincipals
    token_data: JWToken
    token_str: str
    current_user, token_data, token_str = current_user_access_token
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_VERIFIED,
        )
    return current_user, token_data, token_str


async def get_current_active_refresh_user(
    current_user_access_token: Tuple[UserPrincipals, JWToken, str] = Depends(
        get_current_verified_refresh_user
    ),
) -> Tuple[UserPrincipals, JWToken, str]:  # pragma: no cover
    current_user: UserPrincipals
    token_data: JWToken
    token_str: str
    current_user, token_data, token_str = current_user_access_token
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    return current_user, token_data, token_str


# ACCESS
async def get_current_user_access_token(
    token: str = Depends(bearer_transport.scheme),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Tuple[UserPrincipals, JWToken, str]:
    try:
        return await oauth.verify_token(
            token=token,
            audience=[settings.ACCESS_TOKEN_AUDIENCE],
            is_type="access",
            require_fresh=True,
        )
    except AuthException as e:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": status.HTTP_401_UNAUTHORIZED,
                "reason": e.reason,
            },
        )


async def get_current_verified_user(
    current_user_access_token: Tuple[UserPrincipals, JWToken, str] = Depends(
        get_current_user_access_token
    ),
) -> UserPrincipals:  # pragma: no cover
    current_user: UserPrincipals
    token_data: JWToken
    token_str: str
    current_user, token_data, token_str = current_user_access_token
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_VERIFIED,
        )
    return current_user


async def get_current_active_user(
    current_user: UserPrincipals = Depends(get_current_verified_user),
) -> UserPrincipals:  # pragma: no cover
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    return current_user


# PASSWORD RESET
async def get_current_active_password_reset_user(
    token: str = Body(...),
    csrf: str = Body(...),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> User:  # pragma: no cover
    try:
        user: UserRead
        token_data: JWToken
        token_str: str
        user, token_data, token_str = await oauth.verify_token(
            token=token,
            audience=[settings.RESET_PASSWORD_TOKEN_AUDIENCE],
            check_csrf=True,
            token_csrf=csrf,
        )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorCode.USER_NOT_ACTIVE,
            )
        if settings.USERS_REQUIRE_VERIFICATION and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ErrorCode.USER_NOT_VERIFIED,
            )
        db_user: Optional[User] = await oauth.users.read_by_email(
            email=user.email
        )  # pragma: no cover
        if not db_user:  # pragma: no cover
            raise UserNotExists()
        return db_user  # pragma: no cover
    except UserNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.USER_NOT_FOUND,
        )
    except AuthException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": status.HTTP_401_UNAUTHORIZED,
                "reason": e.reason,
            },
        )


# USER PERMISSIONS
def get_active_user_principals(
    user: User = Depends(get_current_active_user),
) -> List[str]:
    if user:
        principals = [Everyone, Authenticated]
        principals.extend(getattr(user, "principals", []))
    else:
        principals = [Everyone]  # pragma: no cover
    return principals


Permission = configure_permissions(get_active_user_principals)


__all__ = [
    "AuthManager",
    "BearerTransport",
    "bearer_transport",
    "DatabaseStrategy",
    "get_active_user_principals",
    "get_current_active_user",
    "get_current_active_refresh_user",
    "get_current_active_password_reset_user",
    "get_current_user_access_token",
    "get_current_user_by_email",
    "get_current_user_for_verification",
    "get_current_user_refresh_token",
    "get_current_verified_refresh_user",
    "get_current_verified_user",
    "get_jwt_strategy",
    "get_token_db",
    "get_database_strategy",
    "get_db_strategy",
    "get_user_auth",
    "get_user_db",
    "get_user_or_404",
    "JWTStrategy",
    "Permission",
]
