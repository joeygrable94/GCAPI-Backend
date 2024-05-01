from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import (
    Client,
    ClientWebsite,
    GoSearchConsoleProperty,
    User,
    UserClient,
    Website,
)
from app.schemas import (
    GoSearchConsolePropertyCreate,
    GoSearchConsolePropertyRead,
    GoSearchConsolePropertyUpdate,
)


class GoSearchConsolePropertyRepository(
    BaseRepository[
        GoSearchConsolePropertyCreate,
        GoSearchConsolePropertyRead,
        GoSearchConsolePropertyUpdate,
        GoSearchConsoleProperty,
    ]
):
    @property
    def _table(self) -> Type[GoSearchConsoleProperty]:  # type: ignore
        return GoSearchConsoleProperty

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        website_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
        if user_id:
            stmt = (
                stmt.join(Website, self._table.website_id == Website.id)
                .join(ClientWebsite, Website.id == ClientWebsite.website_id)
                .join(Client, ClientWebsite.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(Client, GoSearchConsoleProperty.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        if website_id:
            stmt.join(Website, GoSearchConsoleProperty.website_id == Website.id)
            conditions.append(GoSearchConsoleProperty.website_id.like(website_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
