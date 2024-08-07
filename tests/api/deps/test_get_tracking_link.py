import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.tracking_link import create_random_tracking_link

from app.api.deps import get_tracking_link_or_404
from app.api.exceptions.exceptions import InvalidID, TrackingLinkNotExists
from app.core.utilities.uuids import get_uuid_str
from app.models import TrackingLink
from app.schemas import TrackingLinkRead


async def test_get_tracking_link_or_404(db_session: AsyncSession) -> None:
    # Test with valid tracking_link_id
    test_link: TrackingLinkRead = await create_random_tracking_link(db_session)
    result: TrackingLink | None = await get_tracking_link_or_404(
        db_session, test_link.id
    )
    assert isinstance(result, TrackingLink)
    assert result.id == test_link.id

    # Test with invalid tracking_link_id
    fake_link_id: str = "1"
    with pytest.raises(InvalidID):
        await get_tracking_link_or_404(db_session, fake_link_id)

    # Test with invalid tracking_link_id
    fake_clid = get_uuid_str()
    with pytest.raises(TrackingLinkNotExists):
        await get_tracking_link_or_404(db_session, fake_clid)
