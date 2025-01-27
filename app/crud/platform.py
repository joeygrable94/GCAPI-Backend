from uuid import UUID

from sqlalchemy import Select
from sqlalchemy import select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, ClientPlatform, Platform, User, UserClient
from app.schemas import PlatformCreate, PlatformRead, PlatformUpdateAsAdmin


class PlatformRepository(
    BaseRepository[PlatformCreate, PlatformRead, PlatformUpdateAsAdmin, Platform]
):
    @property
    def _table(self) -> Platform:
        return Platform

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        if user_id:
            stmt = (
                stmt.join(ClientPlatform, Platform.id == ClientPlatform.platform_id)
                .join(Client, ClientPlatform.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
                .where(User.id == user_id)
            )
        if client_id:
            stmt = (
                stmt.join(ClientPlatform, Platform.id == ClientPlatform.platform_id)
                .join(Client, ClientPlatform.client_id == Client.id)
                .where(Client.id == client_id)
            )
        if is_active is not None:
            stmt = stmt.where(Platform.is_active == is_active)
        return stmt
