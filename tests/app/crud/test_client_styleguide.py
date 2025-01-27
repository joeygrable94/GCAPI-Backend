import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import ClientStyleguideRepository
from app.models import ClientStyleguide

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: ClientStyleguideRepository = ClientStyleguideRepository(session=db_session)
    assert repo._table is ClientStyleguide
