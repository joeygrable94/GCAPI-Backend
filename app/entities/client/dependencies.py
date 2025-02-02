from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends

from app.entities.api.dependencies import AsyncDatabaseSession
from app.entities.client.crud import Client, ClientRepository
from app.entities.client.errors import ClientNotFound
from app.utilities import parse_id


async def get_client_or_404(
    db: AsyncDatabaseSession,
    client_id: Any,
) -> Client | None:
    """Parses uuid/int and fetches client by id."""
    parsed_id: UUID = parse_id(client_id)
    client_repo: ClientRepository = ClientRepository(session=db)
    client: Client | None = await client_repo.read(entry_id=parsed_id)
    if client is None:
        raise ClientNotFound()
    return client


FetchClientOr404 = Annotated[Client, Depends(get_client_or_404)]
