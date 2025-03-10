import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_user_organization.crud import UserOrganizationRepository
from app.entities.core_user_organization.model import UserOrganization

pytestmark = pytest.mark.anyio


async def test_user_organization_repo_table(db_session: AsyncSession) -> None:
    repo: UserOrganizationRepository = UserOrganizationRepository(session=db_session)
    assert repo._table is UserOrganization
