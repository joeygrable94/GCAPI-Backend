from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

import jwt
from pydantic import SecretStr

from app.core.config import settings
from app.core.utilities import get_int_from_datetime, get_uuid_str
from app.db.schemas import JWToken, UserRead

SecretType = Union[str, SecretStr]


def _get_secret_value(secret: SecretType) -> str:
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()  # pragma: no cover
    return secret


class StrategyDestroyNotSupportedError(Exception):
    pass


class JWTStrategy:
    def __init__(
        self,
        secret: SecretType,
        algorithm: str = "HS256",
        public_key: Optional[SecretType] = None,
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.public_key = public_key

    @property
    def encode_key(self) -> SecretType:
        return self.secret

    @property
    def decode_key(self) -> SecretType:
        return self.public_key or self.secret

    async def read_token(
        self,
        token: str,
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
    ) -> Optional[JWToken]:
        try:
            raw_token: Dict[str, Any] = jwt.decode(
                token,
                _get_secret_value(self.decode_key),
                audience=audience,
                algorithms=[self.algorithm],
            )
            data: JWToken = JWToken(**raw_token)
            return data
        except jwt.PyJWTError:  # pragma: no cover
            pass
        return None  # pragma: no cover

    async def write_token(
        self,
        user: UserRead,
        csrf: str,
        token_type: str = "access",
        audience: List[str] = [settings.ACCESS_TOKEN_AUDIENCE],
        expires: int = settings.ACCESS_TOKEN_LIFETIME,
        freshness: Optional[bool] = None,
    ) -> Optional[Tuple[str, str, datetime]]:
        try:
            jwt_data: JWToken = JWToken(
                type=token_type,
                iss=settings.PROJECT_NAME,
                nbf=get_int_from_datetime(datetime.now(timezone.utc)),
                iat=get_int_from_datetime(datetime.now(timezone.utc)),
                jti=get_uuid_str(),
                sub=str(user.id),
                aud=audience,
                csrf=csrf,
                scopes=user.scopes,
            )
            expire_at: datetime = datetime.now(timezone.utc) + timedelta(
                seconds=expires
            )
            jwt_data.exp = expire_at
            if token_type == "access" and freshness is not None:
                jwt_data.fresh = freshness
            payload: dict = jwt_data.dict(exclude_unset=True, exclude_none=True).copy()
            auth_token: str = jwt.encode(
                payload, _get_secret_value(self.encode_key), algorithm=self.algorithm
            )
            return auth_token, jwt_data.jti, expire_at
        except jwt.PyJWTError:  # pragma: no cover
            pass
        return None  # pragma: no cover

    async def destroy_token(self, token: str) -> None:
        raise StrategyDestroyNotSupportedError(  # pragma: no cover
            "A JWT can't be invalidated: it's valid until it expires."
        )
