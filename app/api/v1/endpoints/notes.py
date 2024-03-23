from typing import Dict

from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonUserQueryParams,
    GetUserQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_current_user,
    get_note_or_404,
    get_permission_controller,
)
from app.api.exceptions import NoteAlreadyExists
from app.core.pagination import PageParams, Paginated
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteSelf,
    AccessRead,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateSelf,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import NoteRepository
from app.models import Note
from app.schemas import NoteCreate, NoteRead, NoteUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="notes:list",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[NoteRead],
)
async def notes_list(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[NoteRead]:
    """Retrieve a paginated list of notes.

    Permissions:
    ------------
    `role=admin|manager` : all notes

    `role=user` : only notes that belong to the user

    Returns:
    --------
    `Paginated[NoteRead]` : a paginated list of notes, optionally filtered

    """
    # formulate the select statement based on the current user's role
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = notes_repo.query_list(user_id=query.user_id)
    else:  # TODO: test
        select_stmt = notes_repo.query_list(user_id=permissions.current_user.id)
    response_out: Paginated[NoteRead] = (
        await permissions.get_paginated_resource_response(
            table_name=Note.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: NoteRead,
                RoleManager: NoteRead,
                RoleClient: NoteRead,
                RoleEmployee: NoteRead,
            },
        )
    )
    return response_out


@router.post(
    "/",
    name="notes:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=NoteRead,
)
async def notes_create(
    note_in: NoteCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> NoteRead:
    """Create a new note.

    Permissions:
    ------------
    any `role` : create a new note, notes belong to one user

    Returns:
    --------
    `NoteRead` : the newly created note

    """
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    data: Dict = note_in.model_dump()
    check_title: str | None = data.get("title")
    if check_title:
        a_note: Note | None = await notes_repo.read_by(
            field_name="title",
            field_value=check_title,
        )
        if a_note:
            raise NoteAlreadyExists()
    new_note: Note = await notes_repo.create(note_in)
    # return role based response
    response_out: NoteRead = permissions.get_resource_response(
        resource=new_note,
        responses={
            RoleUser: NoteRead,
        },
    )
    return response_out


@router.get(
    "/{note_id}",
    name="notes:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=NoteRead,
)
async def notes_read(
    note: Note = Permission([AccessRead, AccessReadSelf], get_note_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> NoteRead:
    """Retrieve a single note by id.

    Permissions:
    ------------
    `role=admin|manager` : read all notes

    `role=user` : read only notes that belong to the user

    Returns:
    --------
    `NoteRead` : the note matching the note_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        user_id=note.user_id,
    )
    # return role based response
    response_out: NoteRead = permissions.get_resource_response(
        resource=note,
        responses={
            RoleUser: NoteRead,
        },
    )
    return response_out


@router.patch(
    "/{note_id}",
    name="notes:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=NoteRead,
)
async def notes_update(
    note_in: NoteUpdate,
    note: Note = Permission([AccessUpdate, AccessUpdateSelf], get_note_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> NoteRead:
    """Update a note by id.

    Permissions:
    ------------
    `role=admin|manager` : update all notes

    `role=user` : update only notes that belong to the user

    Returns:
    --------
    `NoteRead` : the updated note

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=note_in,
        schema_privileges={
            RoleUser: NoteUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        user_id=note.user_id,
    )
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    if note_in.title is not None:
        a_note: Note | None = await notes_repo.read_by(
            field_name="title", field_value=note_in.title
        )
        if a_note:
            raise NoteAlreadyExists()
    updated_note: Note | None = await notes_repo.update(entry=note, schema=note_in)
    # return role based response
    response_out: NoteRead = permissions.get_resource_response(
        resource=updated_note if updated_note else note,
        responses={
            RoleUser: NoteRead,
        },
    )
    return response_out


@router.delete(
    "/{note_id}",
    name="notes:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=None,
)
async def notes_delete(
    note: Note = Permission([AccessDelete, AccessDeleteSelf], get_note_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a note by id.

    Permissions:
    ------------
    `role=admin|manager` : delete all notes

    `role=user` : delete only notes that belong to the user

    Returns:
    --------
    `None`

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        user_id=note.user_id,
    )
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    await notes_repo.delete(entry=note)
    return None
