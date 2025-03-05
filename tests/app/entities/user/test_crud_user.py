import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_user.crud import UserRepository
from app.entities.core_user.model import User
from app.services.clerk.settings import clerk_settings
from tests.utils.users import create_core_user

pytestmark = pytest.mark.anyio


async def test_user_repo_table(db_session: AsyncSession) -> None:
    repo: UserRepository = UserRepository(session=db_session)
    assert repo._table is User


async def test_user_get_privileges(db_session: AsyncSession) -> None:
    await create_core_user(db_session, "employee")
    user_repo: UserRepository = UserRepository(db_session)
    user_employee: User | None = await user_repo.read_by(
        "email", clerk_settings.first_employee
    )
    privileges = user_employee.privileges()

    assert "user:{}".format(user_employee.id) in privileges
