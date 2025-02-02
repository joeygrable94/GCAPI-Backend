from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.client.model import Client
from app.entities.go_ga4.model import GoAnalytics4Property
from app.entities.go_ga4.schemas import (
    GoAnalytics4PropertyCreate,
    GoAnalytics4PropertyRead,
    GoAnalytics4PropertyUpdate,
)
from app.entities.user.model import User
from app.entities.user_client.model import UserClient


class GoAnalytics4PropertyRepository(
    BaseRepository[
        GoAnalytics4PropertyCreate,
        GoAnalytics4PropertyRead,
        GoAnalytics4PropertyUpdate,
        GoAnalytics4Property,
    ]
):
    @property
    def _table(self) -> GoAnalytics4Property:
        return GoAnalytics4Property

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
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
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
