from app.core.crud import BaseRepository
from app.entities.client_website.model import ClientWebsite
from app.entities.client_website.schemas import (
    ClientWebsiteCreate,
    ClientWebsiteRead,
    ClientWebsiteUpdate,
)


class ClientWebsiteRepository(
    BaseRepository[
        ClientWebsiteCreate, ClientWebsiteRead, ClientWebsiteUpdate, ClientWebsite
    ]
):
    @property
    def _table(self) -> ClientWebsite:
        return ClientWebsite
