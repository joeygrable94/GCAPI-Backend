from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, GoAnalytics4Property, User, UserClient
from app.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
)


class GoAnalytics4PropertyRepository(
    BaseRepository[
        GoAnalytics4PropertyCreate,
        GoAnalytics4PropertyRead,
        GoAnalytics4PropertyUpdate,
        GoAnalytics4Property,
    ]
):
    @property
    def _table(self) -> Type[GoAnalytics4Property]:  # type: ignore
        return GoAnalytics4Property

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
        if user_id:
            stmt = (
                stmt.join(Client, GoAnalytics4Property.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(Client, GoAnalytics4Property.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
