from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, User, UserClient
from app.schemas import ClientCreate, ClientRead, ClientUpdate


class ClientRepository(BaseRepository[ClientCreate, ClientRead, ClientUpdate, Client]):
    @property
    def _table(self) -> Type[Client]:  # type: ignore
        return Client

    def query_list(
        self,
        user_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
        if user_id:  # TODO: test
            stmt = stmt.join(UserClient, Client.id == UserClient.client_id).join(
                User, UserClient.user_id == User.id
            )
            conditions.append(User.id.like(user_id))
        # apply conditions
        if len(conditions) > 0:  # TODO: test
            stmt = stmt.where(and_(*conditions))
        return stmt
