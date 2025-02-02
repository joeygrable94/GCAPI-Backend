from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.client.model import Client
from app.entities.tracking_link.model import TrackingLink
from app.entities.tracking_link.schemas import (
    TrackingLinkCreate,
    TrackingLinkRead,
    TrackingLinkUpdate,
)
from app.entities.user.model import User
from app.entities.user_client.model import UserClient


class TrackingLinkRepository(
    BaseRepository[
        TrackingLinkCreate, TrackingLinkRead, TrackingLinkUpdate, TrackingLink
    ]
):
    @property
    def _table(self) -> TrackingLink:
        return TrackingLink

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
        scheme: str | None = None,
        domain: str | None = None,
        destination: str | None = None,
        url_path: str | None = None,
        utm_campaign: str | None = None,
        utm_medium: str | None = None,
        utm_source: str | None = None,
        utm_content: str | None = None,
        utm_term: str | None = None,
        is_active: bool | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(Client, TrackingLink.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            conditions.append(TrackingLink.client_id.like(client_id))
        if scheme:
            conditions.append(TrackingLink.scheme.like(scheme))
        if domain:
            conditions.append(TrackingLink.domain.like(domain))
        if destination:
            conditions.append(TrackingLink.destination.like(destination))
        if url_path:
            conditions.append(TrackingLink.url_path.like(url_path))
        if utm_campaign:
            conditions.append(TrackingLink.utm_campaign.like(utm_campaign))
        if utm_medium:
            conditions.append(TrackingLink.utm_medium.like(utm_medium))
        if utm_source:
            conditions.append(TrackingLink.utm_source.like(utm_source))
        if utm_content:
            conditions.append(TrackingLink.utm_content.like(utm_content))
        if utm_term:
            conditions.append(TrackingLink.utm_term.like(utm_term))
        if is_active is not None:
            conditions.append(TrackingLink.is_active.is_(is_active))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
