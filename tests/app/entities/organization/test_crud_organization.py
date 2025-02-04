import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.organization.crud import OrganizationRepository
from app.entities.organization.model import Organization

pytestmark = pytest.mark.asyncio


async def test_organizations_repo_table(db_session: AsyncSession) -> None:
    repo: OrganizationRepository = OrganizationRepository(session=db_session)
    assert repo._table is Organization
