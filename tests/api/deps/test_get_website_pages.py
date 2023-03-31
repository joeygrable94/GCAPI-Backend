import pytest
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.website_pages import create_random_website_page

from app.api.deps import get_website_page_or_404
from app.core.utilities.uuids import get_uuid_str
from app.models.website_page import WebsitePage
from app.schemas.website_page import WebsitePageRead


async def test_get_website_page_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_page_id
    test_website_page: WebsitePageRead = await create_random_website_page(db_session)
    result: WebsitePage | None = await get_website_page_or_404(
        db_session, test_website_page.id
    )
    assert isinstance(result, WebsitePage)
    assert result.id == test_website_page.id

    # Test with invalid website_page_id
    fake_clid: str = get_uuid_str()
    with pytest.raises(HTTPException):
        await get_website_page_or_404(db_session, fake_clid)

    # Test with no website_page_id
    result = await get_website_page_or_404(db_session)
    assert result is None
