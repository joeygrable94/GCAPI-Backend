from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import ErrorCode
from app.api.exceptions import (
    ClientNotExists,
    EntityIdNotProvided,
    InvalidID,
    WebsiteNotExists,
)
from app.core.utilities.uuids import parse_id
from app.db.repositories import ClientsRepository, WebsitesRepository
from app.db.schemas.client import ClientRead
from app.db.schemas.website import WebsiteRead
from app.db.tables import Client, Website


# fetch client or 404
async def get_client_or_404(
    db: AsyncSession,
    client_id: Any | None = None,
) -> ClientRead | None:  # pragma: no cover
    """Parses uuid/int and fetches client by id."""
    try:
        if client_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(client_id)
        client_repo: ClientsRepository = ClientsRepository(session=db)
        client: Client | None = await client_repo.read(entry_id=parsed_id)
        if not client:
            raise ClientNotExists()
        return ClientRead.from_orm(client)
    except (ClientNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.CLIENT_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None


# fetch website or 404
async def get_website_or_404(
    db: AsyncSession,
    website_id: Any | None = None,
) -> WebsiteRead | None:  # pragma: no cover
    """Parses uuid/int and fetches website by id."""
    try:
        if website_id is None:
            raise EntityIdNotProvided()
        parsed_id: UUID = parse_id(website_id)
        website_repo: WebsitesRepository = WebsitesRepository(session=db)
        website: Website | None = await website_repo.read(entry_id=parsed_id)
        if not website:
            raise WebsiteNotExists()
        return WebsiteRead.from_orm(website)
    except (WebsiteNotExists, InvalidID):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorCode.WEBSITE_NOT_FOUND,
        )
    except EntityIdNotProvided:
        return None
