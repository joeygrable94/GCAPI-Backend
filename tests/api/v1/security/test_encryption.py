from typing import Any
from typing import Dict

from httpx import AsyncClient
from httpx import Response
from sqlalchemy.ext.asyncio import AsyncSession
from tests.utils.utils import random_lower_string

from app.core.security.schemas import EncryptedMessage
from app.core.security.schemas import PlainMessage


async def test_encrypt_decrypt_message_as_admin(
    client: AsyncClient,
    db_session: AsyncSession,
    admin_token_headers: Dict[str, str],
) -> None:
    # encrypt a message
    input_message: PlainMessage = PlainMessage(message=random_lower_string())
    response: Response = await client.post(
        "/encrypt/message",
        headers=admin_token_headers,
        json=input_message.model_dump(),
    )
    data: Dict[str, Any] = response.json()
    encrypted_message = EncryptedMessage.model_validate(data)
    assert 200 <= response.status_code < 300
    assert encrypted_message.message != input_message.message
    # decrypt the message
    response_2: Response = await client.post(
        "/decrypt/message",
        headers=admin_token_headers,
        json=encrypted_message.model_dump(),
    )
    data_2: Dict[str, Any] = response_2.json()
    decrypted_message = PlainMessage.model_validate(data_2)
    assert 200 <= response_2.status_code < 300
    assert decrypted_message.message == input_message.message
