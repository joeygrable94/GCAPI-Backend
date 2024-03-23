from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.crud.base import BaseRepository
from app.models import (
    Client,
    ClientWebsite,
    User,
    UserClient,
    Website,
    WebsiteMap,
    WebsitePage,
)
from app.schemas import WebsitePageCreate, WebsitePageRead, WebsitePageUpdate


class WebsitePageRepository(
    BaseRepository[WebsitePageCreate, WebsitePageRead, WebsitePageUpdate, WebsitePage]
):
    @property
    def _table(self) -> Type[WebsitePage]:  # type: ignore
        return WebsitePage

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        sitemap_id: UUID | None = None,
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
        if website_id:
            stmt = stmt.join(Website, self._table.website_id == Website.id)
            conditions.append(self._table.website_id.like(website_id))
        if sitemap_id:
            stmt = stmt.join(WebsiteMap, self._table.sitemap_id == WebsiteMap.id)
            conditions.append(self._table.sitemap_id.like(sitemap_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
