import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.organization_styleguide.crud import OrganizationStyleguideRepository
from app.entities.organization_styleguide.model import OrganizationStyleguide

pytestmark = pytest.mark.anyio


async def test_organization_platform_repo_table(db_session: AsyncSession) -> None:
    repo: OrganizationStyleguideRepository = OrganizationStyleguideRepository(
        session=db_session
    )
    assert repo._table is OrganizationStyleguide
