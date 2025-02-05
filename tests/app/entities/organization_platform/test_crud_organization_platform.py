import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.organization_platform.crud import OrganizationPlatformRepository
from app.entities.organization_platform.model import OrganizationPlatform

pytestmark = pytest.mark.asyncio


async def test_organization_platform_repo_table(db_session: AsyncSession) -> None:
    repo: OrganizationPlatformRepository = OrganizationPlatformRepository(session=db_session)
    assert repo._table is OrganizationPlatform
