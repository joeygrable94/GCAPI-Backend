from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.core.security import get_current_active_user
from app.db.repositories import WebsitesRepository
from app.db.schemas import UserRead, WebsiteCreate, WebsiteRead, WebsiteUpdate

router: APIRouter = APIRouter()


@router.get(
    "/", response_model=List[WebsiteRead], name="websites:read_websites"
)
async def websites_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserRead = Depends(get_current_active_user),
) -> Union[List[WebsiteRead], List[Any], None]:
    websites_repo: WebsitesRepository = WebsitesRepository(session=db)
    websites = await websites_repo.list(page=page)
    if websites:
        return websites
    return list()


@router.post("/", response_model=WebsiteRead, name="websites:create_website")
async def websites_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    website_in: WebsiteCreate,
    current_user: UserRead = Depends(get_current_active_user),
) -> WebsiteRead:
    websites_repo: WebsitesRepository = WebsitesRepository(session=db)
    website: WebsiteRead = await websites_repo.create(website_in)
    return website


@router.get("/{id}", response_model=WebsiteRead, name="websites:read_website")
async def websites_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(get_current_active_user),
) -> WebsiteRead:
    websites_repo: WebsitesRepository = WebsitesRepository(session=db)
    website: Optional[WebsiteRead] = await websites_repo.read(entry_id=id)
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )
    return website


@router.patch(
    "/{id}", response_model=WebsiteRead, name="websites:update_website"
)
async def websites_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    website_in: WebsiteUpdate,
    current_user: UserRead = Depends(get_current_active_user),
) -> Any:
    websites_repo: WebsitesRepository = WebsitesRepository(session=db)
    website: Optional[WebsiteRead] = await websites_repo.read(entry_id=id)
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )
    website = await websites_repo.update(entry_id=id, schema=website_in)
    return website


@router.delete(
    "/{id}", response_model=WebsiteRead, name="websites:delete_website"
)
async def websites_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID4,
    current_user: UserRead = Depends(get_current_active_user),
) -> Any:
    websites_repo: WebsitesRepository = WebsitesRepository(session=db)
    website: Optional[WebsiteRead] = await websites_repo.read(entry_id=id)
    if not website:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Website not found"
        )
    website = await websites_repo.delete(entry_id=id)
    return website
