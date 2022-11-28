from datetime import datetime
from typing import Optional

from pydantic import UUID4

from app.db.repositories import AccessTokensRepository
from app.db.schemas import AccessTokenCreate, AccessTokenRead, AccessTokenUpdate
from app.db.tables import AccessToken


class DatabaseStrategy:
    def __init__(self, token_db: AccessTokensRepository):
        self.token_repo: AccessTokensRepository = token_db

    async def read_token(
        self,
        token_jti: str,
    ) -> Optional[AccessTokenRead]:  # pragma: no cover
        access_token: Optional[AccessToken] = await self.token_repo.read_by_token(
            token_jti
        )
        if access_token is None:
            return None
        return AccessTokenRead.from_orm(access_token)

    async def write_token(
        self, token_jti: str, user_id: UUID4, csrf: str, expires_at: datetime
    ) -> AccessTokenRead:  # pragma: no cover
        create_access_token = AccessTokenCreate(
            token_jti=token_jti,
            csrf=csrf,
            expires_at=expires_at,
            is_revoked=False,
            user_id=user_id,
        )
        access_token: AccessToken = await self.token_repo.create(
            schema=create_access_token
        )
        return AccessTokenRead.from_orm(access_token)

    async def revoke_token(self, token_jti: str) -> None:  # pragma: no cover
        token: Optional[AccessToken] = await self.token_repo.read_by_token(token_jti)
        if token is not None:
            await self.token_repo.update(
                entry=token, schema=AccessTokenUpdate(is_revoked=True)
            )
        return None

    async def destroy_token(self, token_jti: str) -> None:  # pragma: no cover
        token: Optional[AccessToken] = await self.token_repo.read_by_token(token_jti)
        if token is not None:
            await self.token_repo.delete(entry=token)
        return None
