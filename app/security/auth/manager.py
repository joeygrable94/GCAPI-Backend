from datetime import datetime, timezone
from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.errors import ErrorCode
from app.api.exceptions import InvalidID, UserNotExists
from app.core.config import settings
from app.core.utilities import get_int_from_datetime, get_uuid_str, parse_id
from app.db.repositories import UserRepository
from app.db.schemas import AccessTokenRead, JWToken
from app.db.schemas.user import UserPrincipals
from app.db.tables import User

from .exceptions import (
    AccessTokenRequired,
    CSRFError,
    ExpiredTokenError,
    FreshTokenRequired,
    InvalidTokenUserId,
    InvalidTokenUserNotFound,
    MissingTokenError,
    RefreshTokenRequired,
    RevokedTokenError,
)
from .strategy import DatabaseStrategy, JWTStrategy
from .transport import BearerTransport


class AuthManager:
    def __init__(
        self,
        bearer: BearerTransport,
        jwt: JWTStrategy,
        tokens: DatabaseStrategy,
        user_db: UserRepository,
    ):
        self.bearer = bearer
        self.jwt = jwt
        self.tokens = tokens
        self.users = user_db

    async def certify(
        self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[UserPrincipals]:  # pragma: no cover
        user: Optional[User] = await self.users.authenticate(credentials)
        if not user:
            return None
        return UserPrincipals.from_orm(user)

    async def fetch_user(
        self, email: EmailStr
    ) -> Optional[UserPrincipals]:  # pragma: no cover
        user: Optional[User] = await self.users.read_by_email(email)
        if not user:
            return None
        return UserPrincipals.from_orm(user)

    async def verify_token(
        self,
        token: str,
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
        is_type: str = "access",
        require_fresh: bool = False,
        check_csrf: bool = False,
        token_csrf: Optional[str] = None,
    ) -> Tuple[UserPrincipals, JWToken, str]:  # pragma: no cover
        token_data: Optional[JWToken] = await self.jwt.read_token(token, audience)
        # check token data
        if token_data is None or token_data.sub is None:
            raise MissingTokenError(reason=ErrorCode.TOKEN_INVALID)
        # check token type
        if is_type == "access" and not token_data.type == "access":
            raise AccessTokenRequired(reason=ErrorCode.ACCESS_TOKEN_REQUIRED)
        if is_type == "refresh" and not token_data.type == "refresh":
            raise RefreshTokenRequired(reason=ErrorCode.REFRESH_TOKEN_REQUIRED)
        # check token freshness
        if require_fresh and not token_data.fresh:
            raise FreshTokenRequired(reason=ErrorCode.FRESH_TOKEN_REQUIRED)
        # check token state
        token_state: Optional[AccessTokenRead] = await self.tokens.read_token(
            token_data.jti
        )
        if token_state is None or token_state.is_revoked:
            raise RevokedTokenError(reason=ErrorCode.TOKEN_REVOKED)
        # check token csrf is valid
        if check_csrf and token_csrf is not None and token_csrf != token_state.csrf:
            raise CSRFError(reason=ErrorCode.TOKEN_CSRF_INVALID)
        # check token belongs to user in request
        if str(token_data.sub) != str(token_state.user_id):
            raise InvalidTokenUserId(reason=ErrorCode.BAD_TOKEN_USER)
        # check token not expired
        token_exp: int = get_int_from_datetime(token_data.exp)
        time_now: int = get_int_from_datetime(datetime.now(timezone.utc))
        if token_exp <= time_now:
            raise ExpiredTokenError(reason=ErrorCode.TOKEN_EXPIRED)
        # check if user_id is valid and current_user exists
        try:
            user_id: UUID = parse_id(token_data.sub)
            current_user: Optional[User] = await self.users.read(entry_id=user_id)
            if not current_user:
                raise UserNotExists()
        except (InvalidID, UserNotExists):
            raise InvalidTokenUserNotFound(reason=ErrorCode.USER_NOT_FOUND)
        # return current_user and their token_data
        return UserPrincipals.from_orm(current_user), token_data, token

    async def store_token(
        self,
        user: UserPrincipals,
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
        expires: int = settings.ACCESS_TOKEN_LIFETIME,
        is_refresh: bool = False,
        is_fresh: Optional[bool] = None,
    ) -> Tuple[str, str]:
        token_csrf: str = get_uuid_str()
        token_type: str
        token_aud: List[str]
        lifetime: int
        # check token type
        if is_refresh:
            token_type = "refresh"
            token_aud = [settings.REFRESH_TOKEN_AUDIENCE]
            lifetime = settings.REFRESH_TOKEN_LIFETIME
        else:
            token_type = "access"
            token_aud = audience
            lifetime = expires
        # make token
        token_data: Optional[tuple[str, str, datetime]] = await self.jwt.write_token(
            user=user,
            csrf=token_csrf,
            token_type=token_type,
            audience=token_aud,
            expires=lifetime,
            freshness=is_fresh,
        )
        if not token_data:  # pragma: no cover
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.TOKEN_ERROR,
            )
        token: str
        token_id: str
        token_exp: datetime
        token, token_id, token_exp = token_data
        await self.tokens.write_token(
            token_jti=token_id,
            user_id=user.id,
            csrf=token_csrf,
            expires_at=token_exp,
        )
        return token, token_csrf  # pragma: no cover

    async def destroy_token(self, token_jti: str, delete: bool = False) -> None:
        if delete:
            await self.tokens.destroy_token(token_jti=token_jti)
        else:
            await self.tokens.revoke_token(token_jti=token_jti)
