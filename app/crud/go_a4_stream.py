from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import (
    Client,
    ClientWebsite,
    GoAnalytics4Stream,
    User,
    UserClient,
    Website,
)
from app.models.go_a4 import GoAnalytics4Property
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
    def _table(self) -> Type[GoAnalytics4Stream]:  # type: ignore
        return GoAnalytics4Stream

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        ga4_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
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
            # stmt = stmt.join(Website, GoAnalytics4Stream.website_id == Website.id)
            conditions.append(GoAnalytics4Stream.website_id.like(website_id))
        if ga4_id:
            stmt = stmt.join(
                GoAnalytics4Property,
                GoAnalytics4Stream.ga4_id == GoAnalytics4Property.id,
            )
            conditions.append(GoAnalytics4Stream.ga4_id.like(ga4_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
