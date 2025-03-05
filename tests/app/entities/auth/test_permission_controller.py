import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.dependencies import PermissionController
from app.entities.core_organization.crud import OrganizationRepository
from app.entities.core_user.crud import UserRepository
from app.entities.core_user_organization.crud import UserOrganizationRepository
from tests.utils.users import create_core_user

pytestmark = pytest.mark.anyio


async def test_init_permission_controller(db_session: AsyncSession) -> None:
    user_a = await create_core_user(db_session, "admin")
    perms: PermissionController = PermissionController(db_session, user_a, [])
    assert perms.db == db_session
    assert perms.current_user == user_a
    assert perms.privileges == []
    assert isinstance(perms.user_repo, UserRepository)
    assert isinstance(perms.organization_repo, OrganizationRepository)
    assert isinstance(perms.user_organization_repo, UserOrganizationRepository)
