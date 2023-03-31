from typing import Type

from app.crud.base import BaseRepository
from app.models import ClientWebsite
from app.schemas import ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate


class ClientWebsiteRepository(
    BaseRepository[
        ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate, ClientWebsite
    ]
):
    @property
    def _table(self) -> Type[ClientWebsite]:  # type: ignore
        return ClientWebsite
