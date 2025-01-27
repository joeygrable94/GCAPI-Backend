from app.crud.base import BaseRepository
from app.models import UserClient
from app.schemas import UserClientCreate, UserClientRead, UserClientUpdate


class UserClientRepository(
    BaseRepository[UserClientCreate, UserClientRead, UserClientUpdate, UserClient]
):
    @property
    def _table(self) -> UserClient:
        return UserClient
