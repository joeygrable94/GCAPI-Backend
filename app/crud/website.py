import socket
from typing import Optional, Type

from app.core.config import settings
from app.core.logger import logger
from app.crud.base import BaseRepository
from app.models import Website
from app.schemas import WebsiteCreate, WebsiteRead, WebsiteUpdate


class WebsiteRepository(
    BaseRepository[WebsiteCreate, WebsiteRead, WebsiteUpdate, Website]
):
    @property
    def _table(self) -> Type[Website]:  # type: ignore
        return Website

    async def validate(
        self,
        domain: Optional[str],
    ) -> bool:
        if settings.DEBUG_MODE:
            return True
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
