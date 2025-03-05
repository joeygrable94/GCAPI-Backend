import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.platform.crud import PlatformRepository
from app.entities.platform.model import Platform

pytestmark = pytest.mark.anyio


async def test_organization_platform_repo_table(db_session: AsyncSession) -> None:
    repo: PlatformRepository = PlatformRepository(session=db_session)
    assert repo._table is Platform
