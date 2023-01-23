from typing import Type

from app.db.repositories.base import BaseRepository
from app.db.schemas import ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate
from app.db.tables import ClientWebsite


class ClientsWebsitesRepository(
    BaseRepository[
        ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate, ClientWebsite
    ]
):
    @property
    def _schema_read(self) -> Type[ClientWebsiteRead]:  # type: ignore
        return ClientWebsiteRead

    @property
    def _table(self) -> Type[ClientWebsite]:  # type: ignore
        return ClientWebsite
