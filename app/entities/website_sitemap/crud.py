from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.entities.client.model import Client
from app.entities.client_website.model import ClientWebsite
from app.entities.user.model import User
from app.entities.user_client.model import UserClient
from app.entities.website.model import Website
from app.entities.website_sitemap.model import WebsiteMap
from app.entities.website_sitemap.schemas import (
    WebsiteMapCreate,
    WebsiteMapRead,
    WebsiteMapUpdate,
)
from app.entities.website_sitemap.utilities import (
    check_is_xml_valid_sitemap,
    fetch_url_page_text,
    fetch_url_status_code,
    parse_sitemap_xml,
)


class WebsiteMapRepository(
    BaseRepository[WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate, WebsiteMap]
):
    @property
    def _table(self) -> WebsiteMap:
        return WebsiteMap

    def query_list(
        self,
        user_id: UUID | None = None,
        website_id: UUID | None = None,
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
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

    def is_sitemap_url_xml_valid(
        self,
        url: str,
    ) -> bool:
        try:
            is_valid: bool = False
            status_code: int = fetch_url_status_code(url)
            if status_code != 200:
                return is_valid
            page_text: str = fetch_url_page_text(url)
            page_xml = parse_sitemap_xml(page_text)
            is_valid = check_is_xml_valid_sitemap(page_xml)
            return is_valid
        except Exception:  # pragma: no cover
            return False
