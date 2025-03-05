import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_organization.crud import OrganizationRepository
from app.entities.core_organization.model import Organization

pytestmark = pytest.mark.anyio


async def test_organizations_repo_table(db_session: AsyncSession) -> None:
    repo: OrganizationRepository = OrganizationRepository(session=db_session)
    assert repo._table is Organization
