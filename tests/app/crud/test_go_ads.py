import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoAdsPropertyRepository
from app.models import GoAdsProperty

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: GoAdsPropertyRepository = GoAdsPropertyRepository(session=db_session)
    assert repo._table is GoAdsProperty
