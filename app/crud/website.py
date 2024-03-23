import socket
from typing import List, Optional, Type
from uuid import UUID

from sqlalchemy import BinaryExpression, Select, and_, select as sql_select

from app.core.logger import logger
from app.crud.base import BaseRepository
from app.models import Client, ClientWebsite, User, UserClient, Website
from app.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Type[Website]:  # type: ignore
        return Website

    def query_list(
        self,
        user_id: UUID | None = None,
        client_id: UUID | None = None,
    ) -> Select:
        # create statement joins
        stmt: Select = sql_select(self._table)
        # create conditions
        conditions: List[BinaryExpression[bool]] = []
        # append conditions
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
        # apply conditions
        if len(conditions) > 0:
            stmt = stmt.where(and_(*conditions))
        return stmt

    async def validate(
        self,
        domain: Optional[str],
    ) -> bool:
        try:
            if not domain:
                raise Exception("Domain name is required to validate")
            addr = socket.gethostbyname(domain)
            logger.info(
                f"Validated website domain {domain} at IP address {addr}"
            )  # pragma: no cover
            return True
        except Exception as e:
            logger.info(
                f"Error validating the domain name: {domain}", e
            )  # pragma: no cover
            return False
