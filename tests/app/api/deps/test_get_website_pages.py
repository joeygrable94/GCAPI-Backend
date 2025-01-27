import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_website_page_or_404
from app.api.exceptions.exceptions import EntityNotFound, InvalidID
from app.core.utilities import get_uuid_str
from app.models import WebsitePage
from app.schemas import WebsitePageRead
from tests.utils.website_pages import create_random_website_page


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
    with pytest.raises(EntityNotFound):
        await get_website_page_or_404(db_session, fake_clid)
