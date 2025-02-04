import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.dependencies import PermissionController
from app.entities.organization.crud import OrganizationRepository
from app.entities.user.crud import UserRepository
from app.entities.user.model import User
from app.entities.user_organization.crud import UserOrganizationRepository
from app.services.auth0.settings import auth_settings
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


async def test_init_permission_controller(db_session: AsyncSession) -> None:
    user_a: User = await get_user_by_email(db_session, auth_settings.first_admin)
    perms: PermissionController = PermissionController(db_session, user_a, [])
    assert perms.db == db_session
    assert perms.current_user == user_a
    assert perms.privileges == []
    assert isinstance(perms.user_repo, UserRepository)
    assert isinstance(perms.organization_repo, OrganizationRepository)
    assert isinstance(perms.user_organization_repo, UserOrganizationRepository)
