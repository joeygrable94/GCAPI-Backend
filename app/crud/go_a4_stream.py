from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.crud.base import BaseRepository
from app.models import (
    Client,
    ClientWebsite,
    GoAnalytics4Property,
    GoAnalytics4Stream,
    User,
    UserClient,
    Website,
)
from app.schemas import (
    GoAnalytics4StreamCreate,
    GoAnalytics4StreamRead,
    GoAnalytics4StreamUpdate,
)


class GoAnalytics4StreamRepository(
    BaseRepository[
        GoAnalytics4StreamCreate,
        GoAnalytics4StreamRead,
        GoAnalytics4StreamUpdate,
        GoAnalytics4Stream,
    ]
):
    @property
    def _table(self) -> GoAnalytics4Stream:
        return GoAnalytics4Stream

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        ga4_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(Website, GoAnalytics4Stream.website_id == Website.id)
                .join(ClientWebsite, Website.id == ClientWebsite.website_id)
                .join(Client, ClientWebsite.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if website_id:
            conditions.append(GoAnalytics4Stream.website_id.like(website_id))
        if ga4_id:
            stmt = stmt.join(
                GoAnalytics4Property,
                GoAnalytics4Stream.ga4_id == GoAnalytics4Property.id,
            )
            conditions.append(GoAnalytics4Stream.ga4_id.like(ga4_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
