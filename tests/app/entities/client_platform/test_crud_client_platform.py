import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client_platform.crud import ClientPlatformRepository
from app.entities.client_platform.model import ClientPlatform

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: ClientPlatformRepository = ClientPlatformRepository(session=db_session)
    assert repo._table is ClientPlatform
