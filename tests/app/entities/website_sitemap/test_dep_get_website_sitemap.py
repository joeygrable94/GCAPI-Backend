import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import EntityNotFound, InvalidID
from app.entities.website_sitemap.dependencies import get_website_map_or_404
from app.entities.website_sitemap.model import WebsiteMap
from app.entities.website_sitemap.schemas import WebsiteMapRead
from app.utilities import get_uuid_str
from tests.utils.website_maps import create_random_website_map


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
    with pytest.raises(EntityNotFound):
        await get_website_map_or_404(db_session, fake_clid)
