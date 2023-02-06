from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.exceptions import WebsiteAlreadyExists, WebsiteNotExists
from app.api.utils import get_client_or_404
from app.core.config import Settings, get_settings
from app.core.logger import logger
from app.db.repositories import WebsiteRepository
from app.db.repositories.client_website import ClientWebsiteRepository
from app.db.schemas import (
    ClientRead,
    ClientWebsiteCreate,
    UserAdmin,
    WebsiteCreate,
    WebsiteRead,
    WebsiteUpdate,
)
from app.db.schemas.website import WebsiteReadRelations
from app.db.tables.client_website import ClientWebsite
from app.db.tables.website import Website
from app.security import Permission, get_current_active_user

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="websites:read_websites",
    response_model=List[WebsiteReadRelations],
)
async def websites_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserAdmin = Permission("list", get_current_active_user),
) -> List[WebsiteRead] | List:
    websites_repo: WebsiteRepository = WebsiteRepository(session=db)
    websites: List[Website] | List[None] | None = await websites_repo.list(page=page)
    if websites and len(websites):  # pragma: no cover
        return [WebsiteRead.from_orm(w) for w in websites]
    return []  # pragma: no cover


@router.post(
    "/",
    name="websites:create_website",
    response_model=WebsiteReadRelations,
)
async def websites_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_in: WebsiteCreate,
    client_id: Any | None = None,
    current_user: UserAdmin = Permission("create", get_current_active_user),
    settings: Settings = Depends(get_settings),
) -> WebsiteRead:
    try:  # pragma: no cover
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        data: Dict[str, str] = website_in.dict()
        check_domain: Optional[str] = data.get("domain")
        if check_domain:
            a_site: Optional[Website] = await websites_repo.read_by(
                field_name="domain",
                field_value=check_domain,
            )
            if a_site:
                raise WebsiteAlreadyExists()
        new_site: Website = await websites_repo.create(website_in)
        # check user has permission to assign clients to websites
        client: Optional[ClientRead] = await get_client_or_404(
            db=db, client_id=client_id
        )
        if client is not None:
            client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
                session=db
            )
            client_site_exists: ClientWebsite | None = (
                await client_website_repo.exists_by_two(
                    field_name_a="client_id",
                    field_value_a=client.id,
                    field_name_b="website_id",
                    field_value_b=new_site.id,
                )
            )
            if client_site_exists is None:
                client_site_rel: ClientWebsite = await client_website_repo.create(
                    schema=ClientWebsiteCreate(
                        client_id=client.id, website_id=new_site.id
                    )
                )
                if settings.DEBUG_MODE:
                    logger.info(
                        f"website [{client_site_rel.website_id}] created with association to client [{client_site_rel.client_id}]"  # noqa: E501
                    )
        return WebsiteRead.from_orm(new_site)
    except WebsiteAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Website domain exists"
        )


@router.get(
    "/{id}",
    name="websites:read_website",
    response_model=WebsiteReadRelations,
)
async def websites_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserAdmin = Permission("read", get_current_active_user),
) -> WebsiteRead:
    try:  # pragma: no cover
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        website: Optional[Website] = await websites_repo.read(entry_id=id)
        if not website:
            raise WebsiteNotExists()
        return WebsiteRead.from_orm(website)
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )


@router.patch(
    "/{id}",
    name="websites:update_website",
    response_model=WebsiteReadRelations,
)
async def websites_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    website_in: WebsiteUpdate,
    current_user: UserAdmin = Permission("update", get_current_active_user),
) -> WebsiteRead:
    try:  # pragma: no cover
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        website: Optional[Website] = await websites_repo.read(entry_id=id)
        if not website:
            raise WebsiteNotExists()
        data: Dict = website_in.dict()
        check_domain: Optional[str] = data.get("domain")
        if check_domain:
            domain_found: Optional[Website] = await websites_repo.read_by(
                field_name="domain",
                field_value=check_domain,
            )
            if domain_found:
                raise WebsiteAlreadyExists()
        updated_website: Optional[Website] = await websites_repo.update(
            entry=website, schema=website_in
        )
        if not updated_website:
            raise WebsiteNotExists()
        return WebsiteRead.from_orm(updated_website)
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )
    except WebsiteAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Website domain exists"
        )


@router.delete(
    "/{id}",
    name="websites:delete_website",
    response_model=None,
)
async def websites_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserAdmin = Permission("delete", get_current_active_user),
) -> None:
    try:  # pragma: no cover
        websites_repo: WebsiteRepository = WebsiteRepository(session=db)
        website: Optional[Website] = await websites_repo.read(entry_id=id)
        if not website:
            raise WebsiteNotExists()
        await websites_repo.delete(entry=website)
        return None
    except WebsiteNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )


# websites_clients_read
# websites_sitemaps_read
# websites_pages_read
