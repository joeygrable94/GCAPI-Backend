from datetime import datetime, timezone
from typing import List, Optional, Tuple
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from app.api.errors import ErrorCode
from app.api.exceptions import InvalidID
from app.core.config import settings
from app.core.utilities import get_int_from_datetime, get_uuid_str, parse_id
from app.db.repositories import UsersRepository
from app.db.schemas import AccessTokenRead, JWToken, UserRead
from app.db.tables import User

from .exceptions import (
    AccessTokenRequired,
    FreshTokenRequired,
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
        user_db: UsersRepository,
    ):
        self.bearer = bearer
        self.jwt = jwt
        self.tokens = tokens
        self.users = user_db

    async def certify(self, credentials: OAuth2PasswordRequestForm) -> Optional[User]:
        return await self.users.authenticate(credentials)

    async def verify_token(
        self,
        token: str,
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
        is_type: str = "access",
        require_fresh: bool = False,
        check_csrf: bool = False,
        token_csrf: Optional[str] = None,
    ) -> Tuple[Optional[UUID], Optional[str], Optional[JWToken]]:
        token_data: Optional[JWToken] = await self.jwt.read_token(
            token=token, audience=audience
        )
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

        # TODO: check token state
        token_state: Optional[AccessTokenRead] = await self.tokens.read_token(
            token_jti=token_data.jti
        )
        if token_state is None:
            raise RevokedTokenError(reason=ErrorCode.TOKEN_INVALID)

        # TODO: check token csrf
        if check_csrf and token_csrf is not None:
            print(token_csrf, token_state.csrf)

        # TODO: check token user
        print(token_data.sub, token_state.user_id)

        # TODO: check token expired
        t1: int = get_int_from_datetime(token_data.exp)
        t2: int = get_int_from_datetime(datetime.now(timezone.utc))
        print(token_data.exp, token_state.expires_at)
        print(t1, t2)
        # if t1 <= t2:
        #     raise ExpiredTokenError(reason=ErrorCode.TOKEN_EXPIRED)

        # return valid user id
        try:
            user_id: UUID = parse_id(token_data.sub)
            return user_id, token, token_data
        except InvalidID:
            pass
        return None, None, None

    async def store_token(
        self,
        user: UserRead,
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
        expires: int = settings.ACCESS_TOKEN_LIFETIME,
        is_refresh: bool = False,
        is_fresh: Optional[bool] = None,
    ) -> Tuple[Optional[str], Optional[str]]:
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
        if token_data:
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
            return token, token_csrf
        return None, None

    async def destroy_token(self, token_jti: str, delete: bool = False) -> None:
        if delete:
            await self.tokens.destroy_token(token_jti=token_jti)
        else:
            await self.tokens.revoke_token(token_jti=token_jti)
