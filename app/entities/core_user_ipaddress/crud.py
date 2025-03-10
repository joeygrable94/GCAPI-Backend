from app.core.crud import BaseRepository
from app.entities.core_user_ipaddress.model import UserIpaddress
from app.entities.core_user_ipaddress.schemas import (
    UserIpaddressCreate,
    UserIpaddressRead,
    UserIpaddressUpdate,
)


class UserIpaddressRepository(
    BaseRepository[
        UserIpaddressCreate, UserIpaddressRead, UserIpaddressUpdate, UserIpaddress
    ]
):
    @property
    def _table(self) -> UserIpaddress:
        return UserIpaddress
