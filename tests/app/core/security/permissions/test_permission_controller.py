import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import PermissionController
from app.core.config import settings
from app.crud import ClientRepository, UserClientRepository, UserRepository
from app.models import User
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


async def test_init_permission_controller(db_session: AsyncSession) -> None:
    user_a: User = await get_user_by_email(db_session, settings.auth.first_admin)
    perms: PermissionController = PermissionController(db_session, user_a, [])
    assert perms.db == db_session
    assert perms.current_user == user_a
    assert perms.privileges == []
    assert isinstance(perms.user_repo, UserRepository)
    assert isinstance(perms.client_repo, ClientRepository)
    assert isinstance(perms.user_client_repo, UserClientRepository)
