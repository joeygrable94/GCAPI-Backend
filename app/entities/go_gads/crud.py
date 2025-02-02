from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.client.model import Client
from app.entities.go_gads.model import GoAdsProperty
from app.entities.go_gads.schemas import (
    GoAdsPropertyCreate,
    GoAdsPropertyRead,
    GoAdsPropertyUpdate,
)
from app.entities.user.model import User
from app.entities.user_client.model import UserClient
from app.entities.website_go_gads.model import WebsiteGoAdsProperty


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
            stmt = stmt.join(
                WebsiteGoAdsProperty, GoAdsProperty.id == WebsiteGoAdsProperty.go_ads_id
            )
            conditions.append(WebsiteGoAdsProperty.website_id.like(website_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        print(stmt)
        return stmt
