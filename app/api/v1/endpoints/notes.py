from typing import Dict

from fastapi import APIRouter, Depends

from app.api.deps import (
    AsyncDatabaseSession,
    CurrentUser,
    FetchNoteOr404,
    PermissionController,
    get_async_db,
    get_current_user,
    get_note_or_404,
    get_permission_controller,
)
from app.api.exceptions import NoteAlreadyExists
from app.core.pagination import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
)
from app.core.security import auth
from app.core.security.permissions import (
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
)
from app.crud import NoteRepository
from app.models import Note
from app.schemas import NoteCreate, NoteRead, NoteUpdate

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="notes:list",
    dependencies=[
        Depends(PageParamsFromQuery),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[NoteRead],
)
async def notes_list(
    query: GetPaginatedQueryParams,
    db: AsyncDatabaseSession,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[NoteRead]:
    """Retrieve a paginated list of notes.

    Permissions:
    ------------
    `role=admin|manager` : all notes

    `role=client` : notes they created or notes created in association with their
        client id

    `role=employee|user` : only notes that belong to the user

    Returns:
    --------
    `Paginated[NoteRead]` : a paginated list of notes, optionally filtered

    """
    notes_repo: NoteRepository = NoteRepository(session=db)
    response_out: Paginated[
        NoteRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Note.__tablename__,
        stmt=notes_repo.query_list(),
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: NoteRead,
            RoleManager: NoteRead,
            RoleClient: NoteRead,
            RoleEmployee: NoteRead,
        },
    )
    return response_out


@router.post(
    "/",
    name="notes:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
    ],
    response_model=NoteRead,
)
async def notes_create(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    note_in: NoteCreate,
) -> NoteRead:
    """Create a new note.

    Permissions:
    ------------
    any `role` : create a new note, notes belong to one user

    Returns:
    --------
    `NoteRead` : the newly created note

    """
    notes_repo: NoteRepository = NoteRepository(session=db)
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
    return NoteRead.model_validate(new_note)


@router.get(
    "/{note_id}",
    name="notes:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
    ],
    response_model=NoteRead,
)
async def notes_read(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    note: FetchNoteOr404,
) -> NoteRead:
    """Retrieve a single note by id.

    Permissions:
    ------------
    `role=admin` : read all notes

    `role=manager` : read notes of users with `role=manager|client|employee|user`

    `role=user` : read only notes that belong to the user

    Returns:
    --------
    `NoteRead` : the note matching the note_id

    """
    return NoteRead.model_validate(note)


@router.patch(
    "/{note_id}",
    name="notes:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
    ],
    response_model=NoteRead,
)
async def notes_update(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    note: FetchNoteOr404,
    note_in: NoteUpdate,
) -> NoteRead:
    """Update a note by id.

    Permissions:
    ------------
    `role=admin` : update all notes

    `role=manager` : update notes of users with `role=manager|client|employee|user`

    `role=user` : update only notes that belong to the user

    Returns:
    --------
    `NoteRead` : the updated note

    """
    notes_repo: NoteRepository = NoteRepository(session=db)
    if note_in.title is not None:
        a_note: Note | None = await notes_repo.read_by(
            field_name="title", field_value=note_in.title
        )
        if a_note:
            raise NoteAlreadyExists()
    updated_note: Note | None = await notes_repo.update(entry=note, schema=note_in)
    return (
        NoteRead.model_validate(updated_note)
        if updated_note
        else NoteRead.model_validate(note)
    )


@router.delete(
    "/{note_id}",
    name="notes:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_note_or_404),
    ],
    response_model=None,
)
async def notes_delete(
    current_user: CurrentUser,
    db: AsyncDatabaseSession,
    note: FetchNoteOr404,
) -> None:
    """Delete a note by id.

    Permissions:
    ------------
    `role=admin` : delete all notes

    `role=manager` : delete notes of users with `role=manager|client|employee|user`

    `role=user` : delete only notes that belong to the user

    Returns:
    --------
    `None`

    """
    notes_repo: NoteRepository = NoteRepository(session=db)
    await notes_repo.delete(entry=note)
    return None
