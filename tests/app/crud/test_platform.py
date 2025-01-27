import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import PlatformRepository
from app.models import Platform

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: PlatformRepository = PlatformRepository(session=db_session)
    assert repo._table is Platform
