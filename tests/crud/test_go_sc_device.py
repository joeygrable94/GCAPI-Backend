import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoSearchConsoleDeviceRepository
from app.models import GoSearchConsoleDevice

pytestmark = pytest.mark.asyncio


async def test_go_sc_device_repo_table(db_session: AsyncSession) -> None:
    repo: GoSearchConsoleDeviceRepository = GoSearchConsoleDeviceRepository(
        session=db_session
    )
    assert repo._table is GoSearchConsoleDevice
