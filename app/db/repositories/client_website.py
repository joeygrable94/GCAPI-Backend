from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate
from app.db.tables import ClientWebsite


class ClientWebsiteRepository(
    BaseRepository[
        ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate, ClientWebsite
    ]
):
    @property
    def _table(self) -> Type[ClientWebsite]:  # type: ignore
        return ClientWebsite
