import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.auth.controller import PermissionController
from app.entities.auth.dependencies import get_permission_controller
from tests.constants.schema import ClientAuthorizedUser
from tests.utils.users import get_user_by_email

pytestmark = pytest.mark.asyncio


async def test_get_permission_controller(
    db_session: AsyncSession, admin_user: ClientAuthorizedUser
) -> None:
    this_user = await get_user_by_email(db_session, admin_user.email)
    permission_controller = get_permission_controller(
        db_session,
        this_user,
        ["read:all"],
    )
    assert isinstance(permission_controller, PermissionController)
    assert permission_controller.current_user == this_user
