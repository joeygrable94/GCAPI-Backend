import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import EntityNotFound, InvalidID
from app.entities.tracking_link.dependencies import get_tracking_link_or_404
from app.entities.tracking_link.model import TrackingLink
from app.utilities import get_uuid_str
from tests.utils.clients import create_random_client
from tests.utils.tracking_link import create_random_tracking_link


async def test_get_tracking_link_or_404(db_session: AsyncSession) -> None:
    # Test with valid tracking_link_id
    a_client = await create_random_client(db_session)
    test_link = await create_random_tracking_link(db_session, a_client.id)
    result = await get_tracking_link_or_404(db_session, test_link.id)
    assert isinstance(result, TrackingLink)
    assert result.id == test_link.id

    # Test with invalid tracking_link_id
    fake_link_id: str = "1"
    with pytest.raises(InvalidID):
        await get_tracking_link_or_404(db_session, fake_link_id)

    # Test with invalid tracking_link_id
    fake_clid = get_uuid_str()
    with pytest.raises(EntityNotFound):
        await get_tracking_link_or_404(db_session, fake_clid)
