import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.client_styleguide.crud import ClientStyleguideRepository
from app.entities.client_styleguide.model import ClientStyleguide

pytestmark = pytest.mark.asyncio


async def test_client_platform_repo_table(db_session: AsyncSession) -> None:
    repo: ClientStyleguideRepository = ClientStyleguideRepository(session=db_session)
    assert repo._table is ClientStyleguide
