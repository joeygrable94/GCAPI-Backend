import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.core_geocoord.crud import GeocoordRepository
from app.entities.core_geocoord.model import Geocoord

pytestmark = pytest.mark.anyio


async def test_geocoord_repo_table(db_session: AsyncSession) -> None:
    repo: GeocoordRepository = GeocoordRepository(session=db_session)
    assert repo._table is Geocoord
