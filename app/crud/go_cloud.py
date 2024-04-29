from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, GoCloudProperty, User, UserClient
from app.schemas import (
    GoCloudPropertyCreate,
    GoCloudPropertyRead,
    GoCloudPropertyUpdate,
)


class GoCloudPropertyRepository(
    BaseRepository[
        GoCloudPropertyCreate,
        GoCloudPropertyRead,
        GoCloudPropertyUpdate,
        GoCloudProperty,
    ]
):
    @property
    def _table(self) -> Type[GoCloudProperty]:  # type: ignore
        return GoCloudProperty

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
                stmt.join(Client, GoCloudProperty.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(Client, GoCloudProperty.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
