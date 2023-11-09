import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client

from app.api.deps import get_client_or_404
from app.api.exceptions.exceptions import ClientNotExists
from app.api.exceptions.exceptions import InvalidID
from app.core.utilities.uuids import get_uuid_str
from app.models.client import Client
from app.schemas.client import ClientRead


async def test_get_client_or_404(db_session: AsyncSession) -> None:
    # Test with valid client_id
    test_client: ClientRead = await create_random_client(db_session)
    result: Client | None = await get_client_or_404(db_session, test_client.id)
    assert isinstance(result, Client)
    assert result.id == test_client.id

    # Test with invalid client_id
    fake_clid: str = "1"
    with pytest.raises(InvalidID):
        await get_client_or_404(db_session, fake_clid)

    # Test with invalid client_id
    fake_clid = get_uuid_str()
    with pytest.raises(ClientNotExists):
        await get_client_or_404(db_session, fake_clid)
