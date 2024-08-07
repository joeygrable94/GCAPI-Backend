from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import Client, ClientTrackingLink, TrackingLink, User, UserClient
from app.schemas import TrackingLinkCreate, TrackingLinkRead, TrackingLinkUpdate


class TrackingLinkRepository(
    BaseRepository[
        TrackingLinkCreate, TrackingLinkRead, TrackingLinkUpdate, TrackingLink
    ]
):
    @property
    def _table(self) -> Type[TrackingLink]:  # type: ignore
        return TrackingLink

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        utm_campaign: str | None = None,
        utm_medium: str | None = None,
        utm_source: str | None = None,
        utm_content: str | None = None,
        utm_term: str | None = None,
        is_active: bool | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
        if user_id:
            stmt = (
                stmt.join(
                    ClientTrackingLink,
                    self._table.id == ClientTrackingLink.tracking_link_id,
                )
                .join(Client, ClientTrackingLink.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(
                ClientTrackingLink,
                self._table.id == ClientTrackingLink.tracking_link_id,
            ).join(Client, ClientTrackingLink.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        if utm_campaign:
            conditions.append(self._table.utm_campaign.like(utm_campaign))
        if utm_medium:
            conditions.append(self._table.utm_medium.like(utm_medium))
        if utm_source:
            conditions.append(self._table.utm_source.like(utm_source))
        if utm_content:
            conditions.append(self._table.utm_content.like(utm_content))
        if utm_term:
            conditions.append(self._table.utm_term.like(utm_term))
        if is_active is not None:
            conditions.append(self._table.is_active.is_(is_active))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
