import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_maps import create_random_website_map

from app.api.deps import get_website_map_or_404
from app.api.exceptions.exceptions import InvalidID, WebsiteMapNotExists
from app.core.utilities import get_uuid_str
from app.models import WebsiteMap
from app.schemas import WebsiteMapRead


async def test_get_website_map_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_map_id
    test_website_map: WebsiteMapRead = await create_random_website_map(db_session)
    result: WebsiteMap | None = await get_website_map_or_404(
        db_session, test_website_map.id
    )
    assert isinstance(result, WebsiteMap)
    assert result.id == test_website_map.id

    # Test with invalid website_map_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_website_map_or_404(db_session, fake_clid)

    fake_clid = get_uuid_str()
    with pytest.raises(WebsiteMapNotExists):
        await get_website_map_or_404(db_session, fake_clid)
