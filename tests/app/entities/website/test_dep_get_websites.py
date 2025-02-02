import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import EntityNotFound, InvalidID
from app.entities.website.dependencies import get_website_or_404
from app.entities.website.model import Website
from app.utilities import get_uuid_str
from tests.utils.websites import create_random_website


async def test_get_website_or_404(db_session: AsyncSession) -> None:
    # Test with valid website_id
    test_website = await create_random_website(db_session)
    result: Website | None = await get_website_or_404(db_session, test_website.id)
    assert isinstance(result, Website)
    assert result.id == test_website.id

    # Test with invalid website_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_website_or_404(db_session, fake_clid)

    fake_clid = get_uuid_str()
    with pytest.raises(EntityNotFound):
        await get_website_or_404(db_session, fake_clid)
