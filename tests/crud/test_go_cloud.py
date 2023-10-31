import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import GoCloudPropertyRepository
from app.models import GoCloudProperty

pytestmark = pytest.mark.asyncio


async def test_go_cloud_repo_table(db_session: AsyncSession) -> None:
    repo: GoCloudPropertyRepository = GoCloudPropertyRepository(session=db_session)
    assert repo._table is GoCloudProperty
