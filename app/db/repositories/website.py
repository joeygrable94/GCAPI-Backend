from typing import Type, final
import socket

from pydantic import AnyHttpUrl

from app.core.logger import logger
from app.db.repositories.base import BaseRepository
from app.db.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate
from app.db.tables import Website


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Type[Website]:  # type: ignore
        return Website

    async def validate(
        self, domain: AnyHttpUrl,
    ) -> bool:
        try:
            addr = socket.gethostbyname(domain)
            logger.info(f"Validated website domain {domain} at IP address {addr}")
            return True
        except Exception as e:
            logger.info(f"Error validating the domain name: {domain}", e)
            return False
