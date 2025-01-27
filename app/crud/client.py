from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, User, UserClient
from app.schemas import ClientCreate, ClientRead, ClientUpdate


class ClientRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _table(self) -> Client:
        return Client

    def query_list(
        self,
        user_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = stmt.join(UserClient, Client.id == UserClient.client_id).join(
                User, UserClient.user_id == User.id
            )
            conditions.append(User.id.like(user_id))
        if is_active is not None:
            stmt = stmt.where(Client.is_active == is_active)
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
