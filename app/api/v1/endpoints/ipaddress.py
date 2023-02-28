from typing import Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_async_db
from app.api.exceptions import EntityAlreadyExists, EntityNotExists
from app.db.repositories import IpAddressRepository
from app.db.schemas import (
    IpAddressCreate,
    IpAddressRead,
    IpAddressReadRelations,
    IpAddressUpdate,
    UserPrincipals,
)
from app.db.tables import IpAddress
from app.security import Permission, get_current_active_user

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="ipaddress:read_ipaddress_list",
    response_model=List[IpAddressReadRelations],
)
async def ipaddress_list(
    db: AsyncSession = Depends(get_async_db),
    page: int = 1,
    current_user: UserPrincipals = Permission("list", get_current_active_user),
) -> List[IpAddressRead] | List:
    ipaddress_repo: IpAddressRepository = IpAddressRepository(session=db)
    ipaddress: List[IpAddress] | List[None] | None = await ipaddress_repo.list(
        page=page
    )
    if ipaddress and len(ipaddress):  # pragma: no cover
        return [IpAddressRead.from_orm(c) for c in ipaddress]
    return []  # pragma: no cover


@router.post(
    "/",
    name="ipaddress:create_ipaddress",
    response_model=IpAddressReadRelations,
)
async def ipaddress_create(
    *,
    db: AsyncSession = Depends(get_async_db),
    ipaddress_in: IpAddressCreate,
    current_user: UserPrincipals = Permission("create", get_current_active_user),
) -> IpAddressRead:
    try:
        ipaddress_repo: IpAddressRepository = IpAddressRepository(session=db)
        data: Dict = ipaddress_in.dict()
        check_address: Optional[str] = data.get("address")
        if check_address:
            a_ipaddress: Optional[IpAddress] = await ipaddress_repo.read_by(
                field_name="address",
                field_value=check_address,
            )
            if a_ipaddress:  # pragma: no cover
                raise EntityAlreadyExists()
        new_ipaddress: IpAddress = await ipaddress_repo.create(
            ipaddress_in
        )  # pragma: no cover
        return IpAddressRead.from_orm(new_ipaddress)  # pragma: no cover
    except EntityAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="IpAddress exists"
        )


@router.get(
    "/{id}",
    name="ipaddress:read_ipaddress",
    response_model=IpAddressReadRelations,
)
async def ipaddress_read(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserPrincipals = Permission("read", get_current_active_user),
) -> IpAddressRead:
    try:  # pragma: no cover
        ipaddress_repo: IpAddressRepository = IpAddressRepository(session=db)
        ipaddress: Optional[IpAddress] = await ipaddress_repo.read(entry_id=id)
        if not ipaddress:
            raise EntityNotExists()
        return IpAddressRead.from_orm(ipaddress)
    except EntityNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="IpAddress not found"
        )


@router.patch(
    "/{id}",
    name="ipaddress:update_ipaddress",
    response_model=IpAddressReadRelations,
)
async def ipaddress_update(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    ipaddress_in: IpAddressUpdate,
    current_user: UserPrincipals = Permission("update", get_current_active_user),
) -> IpAddressRead:
    try:  # pragma: no cover
        ipaddress_repo: IpAddressRepository = IpAddressRepository(session=db)
        ipaddress: Optional[IpAddress] = await ipaddress_repo.read(entry_id=id)
        if not ipaddress:
            raise EntityNotExists()
        data: Dict = ipaddress_in.dict()
        check_address: Optional[str] = data.get("address")
        if check_address:
            a_ipaddress = await ipaddress_repo.read_by(
                field_name="address", field_value=check_address
            )
            if a_ipaddress:
                raise EntityAlreadyExists()
        updated_ipaddress: Optional[IpAddress] = await ipaddress_repo.update(
            entry=ipaddress, schema=ipaddress_in
        )
        if not updated_ipaddress:
            raise EntityNotExists()
        return IpAddressRead.from_orm(updated_ipaddress)
    except EntityNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="IpAddress not found"
        )
    except EntityAlreadyExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="IpAddress exists"
        )


@router.delete(
    "/{id}",
    name="ipaddress:delete_ipaddress",
    response_model=None,
)
async def ipaddress_delete(
    *,
    db: AsyncSession = Depends(get_async_db),
    id: UUID,
    current_user: UserPrincipals = Permission("delete", get_current_active_user),
) -> None:  # pragma: no cover
    try:
        ipaddress_repo: IpAddressRepository = IpAddressRepository(session=db)
        ipaddress: Optional[IpAddress] = await ipaddress_repo.read(entry_id=id)
        if not ipaddress:
            raise EntityNotExists()
        await ipaddress_repo.delete(entry=ipaddress)
        return None
    except EntityNotExists:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="IpAddress not found"
        )
