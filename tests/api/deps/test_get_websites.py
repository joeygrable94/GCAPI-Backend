import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.websites import create_random_website

from app.api.deps import get_website_or_404
from app.api.exceptions.exceptions import InvalidID, WebsiteNotExists
from app.core.utilities.uuids import get_uuid_str
from app.models.website import Website
from app.schemas.website import WebsiteRead


async def test_get_website_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_id
    test_website: Website | WebsiteRead = await create_random_website(db_session)
    result: Website | None = await get_website_or_404(db_session, test_website.id)
    assert isinstance(result, Website)
    assert result.id == test_website.id

    # Test with invalid website_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_website_or_404(db_session, fake_clid)

    fake_clid = get_uuid_str()
    with pytest.raises(WebsiteNotExists):
        await get_website_or_404(db_session, fake_clid)
