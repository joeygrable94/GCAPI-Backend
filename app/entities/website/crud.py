import socket
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_
from sqlalchemy import select as sql_select

from app.core.crud import BaseRepository
from app.core.logger import logger
from app.entities.client.model import Client
from app.entities.client_website.model import ClientWebsite
from app.entities.user.model import User
from app.entities.user_client.model import UserClient
from app.entities.website.model import Website
from app.entities.website.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Website:
        return Website

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
    ) -> Select:
        stmt: Select = sql_select(self._table)
        conditions: list[BinaryExpression[bool]] = []
        if user_id:
            stmt = (
                stmt.join(ClientWebsite, self._table.id == ClientWebsite.website_id)
                .join(Client, ClientWebsite.client_id == Client.id)
                .join(UserClient, Client.id == UserClient.client_id)
                .join(User, UserClient.user_id == User.id)
            )
            conditions.append(User.id.like(user_id))
        if client_id:
            stmt = stmt.join(
                ClientWebsite, self._table.id == ClientWebsite.website_id
            ).join(Client, ClientWebsite.client_id == Client.id)
            conditions.append(Client.id.like(client_id))
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

    async def validate(
        self,
        domain: str | None,
    ) -> bool:
        try:
            if not domain:
                raise Exception()
            addr = socket.gethostbyname(domain)
            logger.info(
                f"Validated website domain {domain} at IP address {addr}"
            )  # pragma: no cover
            return True
        except Exception:
            logger.info(
                f"Error validating the domain name: {domain}"
            )  # pragma: no cover
            return False
