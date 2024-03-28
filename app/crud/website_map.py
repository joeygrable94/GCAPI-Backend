from typing import List, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.core import logger
from app.core.utilities import (
    check_is_xml_valid_sitemap,
    fetch_url_page_text,
    fetch_url_status_code,
    parse_sitemap_xml,
)
from app.crud.base import BaseRepository
from app.models import Client, ClientWebsite, User, UserClient, Website, WebsiteMap
from app.schemas import WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate


class WebsiteMapRepository(
    BaseRepository[WebsiteMapCreate, WebsiteMapRead, WebsiteMapUpdate, WebsiteMap]
):
    @property
    def _table(self) -> Type[WebsiteMap]:  # type: ignore
        return WebsiteMap

    def query_list(
        self,
        user_id: UUID | None = None,
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
        if website_id:
            stmt = stmt.join(Website, self._table.website_id == Website.id)
            conditions.append(self._table.website_id.like(website_id))
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

    async def is_sitemap_url_xml_valid(
        self,
        url: str,
    ) -> bool:
        is_valid: bool = False
        try:
            # check if the URL is valid
            status_code: int = await fetch_url_status_code(url)
            if status_code != 200:
                return is_valid
            page_text: str = await fetch_url_page_text(url)
            page_xml = await parse_sitemap_xml(page_text)
            is_valid = await check_is_xml_valid_sitemap(page_xml)
            if not is_valid:  # pragma: no cover
                raise Exception("Invalid Sitemap XML")
        except Exception as e:  # pragma: no cover
            logger.info("Error Fetching Sitemap Url: %s" % e)
        finally:
            return is_valid
