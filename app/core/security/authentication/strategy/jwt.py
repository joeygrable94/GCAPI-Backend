from typing import Generic, List, Optional

import jwt

from app.api.exceptions import InvalidID, UserNotExists
from app.core.security.authentication.strategy.base import (
    Strategy,
    StrategyDestroyNotSupportedError,
)
from app.core.security.jwt import SecretType, decode_jwt, generate_jwt
from app.core.security.manager import UserManager
from app.db.schemas.user import ID, UP


class JWTStrategy(Strategy[UP, ID], Generic[UP, ID]):
    def __init__(
        self,
        secret: SecretType,
        lifetime_seconds: Optional[int],
        token_audience: List[str] = ["users:auth"],
        algorithm: str = "HS256",
        public_key: Optional[SecretType] = None,
    ):
        self.secret = secret
        self.lifetime_seconds = lifetime_seconds
        self.token_audience = token_audience
        self.algorithm = algorithm
        self.public_key = public_key

    @property
    def encode_key(self) -> SecretType:
        return self.secret

    @property
    def decode_key(self) -> SecretType:
        return self.public_key or self.secret

    async def read_token(
        self, token: Optional[str], user_manager: UserManager[UP, ID]
    ) -> Optional[UP]:
        if token is None:
            return None

        try:
            data = decode_jwt(
                token, self.decode_key, self.token_audience, algorithms=[self.algorithm]
            )
            user_id = data.get("user_id")
            if user_id is None:
                return None
        except jwt.PyJWTError:
            return None

        try:
            parsed_id = user_manager.parse_id(user_id)
            return await user_manager.get(parsed_id)
        except (UserNotExists, InvalidID):
            return None

    async def write_token(self, user: UP) -> str:
        data = {"user_id": str(user.id), "aud": self.token_audience}
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )

    async def destroy_token(self, token: str, user: UP) -> None:
        raise StrategyDestroyNotSupportedError(
            "A JWT can't be invalidated: it's valid until it expires."
        )
