import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.user_organization.crud import UserOrganizationRepository
from app.entities.user_organization.model import UserOrganization

pytestmark = pytest.mark.asyncio


async def test_user_organization_repo_table(db_session: AsyncSession) -> None:
    repo: UserOrganizationRepository = UserOrganizationRepository(session=db_session)
    assert repo._table is UserOrganization
