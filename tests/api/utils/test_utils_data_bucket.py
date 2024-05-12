import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.clients import create_random_client
from tests.utils.utils import random_lower_string

from app.api.utilities import create_or_read_data_bucket
from app.models import DataBucket
from app.schemas import ClientRead

pytestmark = pytest.mark.asyncio


async def test_create_or_read_data_bucket_create(
    db_session: AsyncSession,
) -> None:
    client: ClientRead = await create_random_client(db_session)
    random_prefix = random_lower_string(64)
    output = await create_or_read_data_bucket(random_prefix, str(client.id), None, None)
    assert output is not None
    assert isinstance(output, DataBucket)


async def test_create_or_read_data_bucket_create_then_read(
    db_session: AsyncSession,
) -> None:
    client: ClientRead = await create_random_client(db_session)
    random_prefix = random_lower_string(64)
    output = await create_or_read_data_bucket(random_prefix, str(client.id), None, None)
    assert output is not None
    assert isinstance(output, DataBucket)
    output_2 = await create_or_read_data_bucket(
        random_prefix, str(client.id), None, None
    )
    assert output_2 is not None
    assert isinstance(output_2, DataBucket)
    assert output.id == output_2.id


async def test_create_or_read_data_bucket_bad_client_id(
    db_session: AsyncSession,
) -> None:
    bad_client_id = 12345
    random_prefix = random_lower_string(64)
    output = await create_or_read_data_bucket(
        random_prefix, str(bad_client_id), None, None
    )
    assert output is None
