import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GeocoordRepository
from app.models import Geocoord

pytestmark = pytest.mark.asyncio


async def test_geocoord_repo_table(db_session: AsyncSession) -> None:
    repo: GeocoordRepository = GeocoordRepository(session=db_session)
    assert repo._table is Geocoord
