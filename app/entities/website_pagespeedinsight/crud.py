from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.client.model import Client
from app.entities.client_website.model import ClientWebsite
from app.entities.user.model import User
from app.entities.user_client.model import UserClient
from app.entities.website.model import Website
from app.entities.website_page.model import WebsitePage
from app.entities.website_pagespeedinsight.model import WebsitePageSpeedInsights
from app.entities.website_pagespeedinsight.schemas import (
    WebsitePageSpeedInsightsCreate,
    WebsitePageSpeedInsightsRead,
    WebsitePageSpeedInsightsUpdate,
)


class WebsitePageSpeedInsightsRepository(
    BaseRepository[
        WebsitePageSpeedInsightsCreate,
        WebsitePageSpeedInsightsRead,
        WebsitePageSpeedInsightsUpdate,
        WebsitePageSpeedInsights,
    ]
):
    @property
    def _table(self) -> WebsitePageSpeedInsights:
        return WebsitePageSpeedInsights

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
        page_id: UUID | None = None,
        devices: list[str] | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
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
        if page_id:
            stmt = stmt.join(WebsitePage, self._table.page_id == WebsitePage.id)
            conditions.append(self._table.page_id.like(page_id))
        if devices:
            conditions.append(self._table.strategy.in_(iter(devices)))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt
