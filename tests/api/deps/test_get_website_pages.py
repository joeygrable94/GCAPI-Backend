import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page

from app.api.deps import get_website_page_or_404
from app.api.exceptions.exceptions import InvalidID, WebsitePageNotExists
from app.core.utilities.uuids import get_uuid_str
from app.models import WebsitePage
from app.schemas import WebsitePageRead


async def test_get_website_page_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_page_id
    test_website_page: WebsitePageRead = await create_random_website_page(db_session)
    result: WebsitePage | None = await get_website_page_or_404(
        db_session, test_website_page.id
    )
    assert isinstance(result, WebsitePage)
    assert result.id == test_website_page.id

    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_website_page_or_404(db_session, fake_clid)

    # Test with invalid website_page_id
    fake_clid = get_uuid_str()
    with pytest.raises(WebsitePageNotExists):
        await get_website_page_or_404(db_session, fake_clid)
