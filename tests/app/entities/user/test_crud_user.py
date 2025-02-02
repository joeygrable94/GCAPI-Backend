import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user.crud import UserRepository
from app.entities.user.model import User
from app.services.auth0.settings import auth_settings

pytestmark = pytest.mark.asyncio


async def test_user_repo_table(db_session: AsyncSession) -> None:
    repo: UserRepository = UserRepository(session=db_session)
    assert repo._table is User


async def test_user_get_privileges(db_session: AsyncSession) -> None:
    user_repo: UserRepository = UserRepository(db_session)
    user_employee: User | None = await user_repo.read_by(
        "email", auth_settings.first_employee
    )
    privileges = user_employee.privileges()

    assert "user:{}".format(user_employee.id) in privileges
