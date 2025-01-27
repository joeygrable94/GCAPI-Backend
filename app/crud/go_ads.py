from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, GoAdsProperty, User, UserClient
from app.schemas import GoAdsPropertyCreate, GoAdsPropertyRead, GoAdsPropertyUpdate


class GoAdsPropertyRepository(
    BaseRepository[
        GoAdsPropertyCreate,
        GoAdsPropertyRead,
        GoAdsPropertyUpdate,
        GoAdsProperty,
    ]
):
    @property
    def _table(self) -> GoAdsProperty:
        return GoAdsProperty

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        website_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(Client, GoAdsProperty.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(Client, GoAdsProperty.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        if website_id:
            conditions.append(GoAdsProperty.website_id.like(website_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
