import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.go_gads.crud import GoAdsPropertyRepository
from app.entities.go_gads.model import GoAdsProperty

pytestmark = pytest.mark.asyncio


async def test_organization_platform_repo_table(db_session: AsyncSession) -> None:
    repo: GoAdsPropertyRepository = GoAdsPropertyRepository(session=db_session)
    assert repo._table is GoAdsProperty
