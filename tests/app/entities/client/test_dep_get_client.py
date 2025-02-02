import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.api.errors import InvalidID
from app.entities.client.dependencies import get_client_or_404
from app.entities.client.errors import ClientNotFound
from app.entities.client.model import Client
from app.utilities import get_uuid_str
from tests.utils.clients import create_random_client

pytestmark = pytest.mark.asyncio


async def test_get_client_or_404(db_session: AsyncSession) -> None:
    # Test with valid client_id
    test_client = await create_random_client(db_session)
    result = await get_client_or_404(db_session, test_client.id)
    assert isinstance(result, Client)
    assert result.id == test_client.id

    # Test with invalid client_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_client_or_404(db_session, fake_clid)

    # Test with invalid client_id
    fake_clid = get_uuid_str()
    with pytest.raises(ClientNotFound):
        await get_client_or_404(db_session, fake_clid)
