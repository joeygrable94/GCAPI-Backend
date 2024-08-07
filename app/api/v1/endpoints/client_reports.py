from fastapi import APIRouter, Depends
from sqlalchemy import Select

from app.api.deps import (
    Permission,
    PermissionController,
    get_async_db,
    get_client_or_404,
    get_client_report_or_404,
    get_current_user,
    get_permission_controller,
)
from app.api.exceptions import (
    ClientNotExists,
    ClientReportAlreadyExists,
    NoteAlreadyExists,
)
from app.core.pagination import (
    GetPaginatedQueryParams,
    PageParams,
    PageParamsFromQuery,
    Paginated,
)
from app.core.security import auth
from app.core.security.permissions import (
    AccessDelete,
    AccessDeleteRelated,
    AccessDeleteSelf,
    AccessRead,
    AccessReadRelated,
    AccessReadSelf,
    AccessUpdate,
    AccessUpdateRelated,
    AccessUpdateSelf,
    RoleAdmin,
    RoleClient,
    RoleEmployee,
    RoleManager,
    RoleUser,
)
from app.crud import ClientReportNoteRepository, ClientReportRepository, NoteRepository
from app.models import Client, ClientReport, Note
from app.schemas import (
    ClientReportCreate,
    ClientReportNoteCreate,
    ClientReportRead,
    ClientReportUpdate,
    NoteCreate,
    NoteRead,
)

router: APIRouter = APIRouter()


@router.get(
    "/{client_id}",
    name="client_reports:list",
    dependencies=[
        Depends(PageParamsFromQuery),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_or_404),
    ],
    response_model=Paginated[ClientReportRead],
)
async def client_report_list(
    query: GetPaginatedQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
    client: Client = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_or_404
    ),
) -> Paginated[ClientReportRead]:
    """Retrieve a paginated list of client reports.

    Permissions:
    ------------
    `role=admin|manager` : all client report

    `role=user` : only client reports associated with the current user

    Returns:
    --------
    `Paginated[ClientReportRead]` : a paginated list of client reports,
        optionally filtered

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # formulate the select statement based on the current user's role
    select_stmt: Select
    report_report = ClientReportRepository(session=permissions.db)
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = report_report.query_list(client_id=client.id)
    else:
        select_stmt = report_report.query_list(
            client_id=client.id, user_id=permissions.current_user.id
        )
    # return role based response
    response_out: Paginated[ClientReportRead] = (
        await permissions.get_paginated_resource_response(
            table_name=ClientReport.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleAdmin: ClientReportRead,
                RoleManager: ClientReportRead,
                RoleClient: ClientReportRead,
                RoleEmployee: ClientReportRead,
            },
        )
    )
    return response_out


@router.post(
    "/{client_id}",
    name="client_reports:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_or_404),
    ],
    response_model=ClientReportRead,
)
async def client_report_create(
    client_report_in: ClientReportCreate,
    client: Client = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientReportRead:
    """Create a new client report.

    Permissions:
    ------------
    `role=admin|manager` : create a new client report for all clients

    `role=user` : create only client reports associated with the current user

    Returns:
    --------
    `ClientReportRead` : the newly created client

    """
    # verify current user has permission to take this action
    if client_report_in.client_id != client.id:
        raise ClientNotExists()
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report_in.client_id,
    )
    report_repo: ClientReportRepository = ClientReportRepository(session=permissions.db)
    a_client_title: ClientReport | None = await report_repo.read_by(
        field_name="title",
        field_value=client_report_in.title,
    )
    a_client_url: ClientReport | None = await report_repo.read_by(
        field_name="url",
        field_value=client_report_in.url,
    )
    if a_client_title is not None or a_client_url is not None:
        raise ClientReportAlreadyExists()
    new_client: ClientReport = await report_repo.create(client_report_in)
    # return role based response
    response_out: ClientReportRead = permissions.get_resource_response(
        resource=new_client,
        responses={
            RoleUser: ClientReportRead,
        },
    )
    return response_out


@router.get(
    "/{client_id}/{report_id}",
    name="client_reports:read",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_or_404),
        Depends(get_client_report_or_404),
    ],
    response_model=ClientReportRead,
)
async def client_report_read(
    client_report: ClientReport = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_report_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientReportRead:
    """Retrieve a single client report by id.

    Permissions:
    ------------
    `role=admin|manager` : all client reports

    `role=user` : only client reports associated with the current user

    Returns:
    --------
    `ClientReportRead` : a client report matching the client_id

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report.client_id,
    )
    # return role based response
    response_out: ClientReportRead = permissions.get_resource_response(
        resource=client_report,
        responses={
            RoleUser: ClientReportRead,
        },
    )
    return response_out


@router.patch(
    "/{client_id}/{report_id}",
    name="client_reports:update",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_report_or_404),
    ],
    response_model=ClientReportRead,
)
async def client_report_update(
    report_in: ClientReportUpdate,
    client_report: ClientReport = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_client_report_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientReportRead:
    """Update a client report by id.

    Permissions:
    ------------
    `role=admin|manager` : all client reports

    `role=user` : only client reports associated with the current user

    Returns:
    --------
    `ClientReportRead` : the updated client report

    """
    # verify the input schema is valid for the current user's role
    permissions.verify_input_schema_by_role(
        input_object=report_in,
        schema_privileges={
            RoleUser: ClientReportUpdate,
        },
    )
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report.client_id,
    )
    if report_in.client_id is not None:
        a_client: Client | None = await permissions.client_repo.read(
            report_in.client_id
        )
        if a_client is None:
            raise ClientNotExists()
        await permissions.verify_user_can_access(
            privileges=[RoleAdmin, RoleManager],
            client_id=report_in.client_id,
        )
    report_repo: ClientReportRepository = ClientReportRepository(session=permissions.db)
    if report_in.title is not None:
        a_client_title: ClientReport | None = await report_repo.read_by(
            field_name="title", field_value=report_in.title
        )
        if a_client_title:
            raise ClientReportAlreadyExists()
    if report_in.url is not None:
        a_client_url: ClientReport | None = await report_repo.read_by(
            field_name="url", field_value=report_in.url
        )
        if a_client_url:
            raise ClientReportAlreadyExists()
    updated_report: ClientReport | None = await report_repo.update(
        entry=client_report, schema=report_in
    )
    # return role based response
    response_out: ClientReportRead = permissions.get_resource_response(
        resource=updated_report if updated_report else client_report,
        responses={
            RoleUser: ClientReportRead,
        },
    )
    return response_out


@router.delete(
    "/{client_id}/{report_id}",
    name="client_reports:delete",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_report_or_404),
    ],
    response_model=None,
)
async def client_report_delete(
    client_report: ClientReport = Permission(
        [AccessDelete, AccessDeleteSelf, AccessDeleteRelated], get_client_report_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> None:
    """Delete a client report by id.

    Permissions:
    ------------
    `role=admin|manager` : delete any client reports

    `role=user` : delete only client reports associated with the current user

    Returns:
    --------
    `None`

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report.client_id,
    )
    report_repo: ClientReportRepository = ClientReportRepository(permissions.db)
    await report_repo.delete(entry=client_report)
    return None


# client report relationships


@router.get(
    "/{client_id}/{report_id}/notes",
    name="client_report_notes:list",
    dependencies=[
        Depends(PageParamsFromQuery),
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_or_404),
        Depends(get_client_report_or_404),
    ],
    response_model=Paginated[NoteRead],
)
async def client_report_note_list(
    query: GetPaginatedQueryParams,
    client_report: ClientReport = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_report_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[NoteRead]:
    """Creates a new note and assigns it to the client report.

    Permissions:
    ------------
    `role=admin|manager` : all client report notes

    `role=user` : only client report notes associated with the current user

    Returns:
    --------
    `Paginated[NoteRead]` : paginated list of client report notes

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report.client_id,
    )
    # formulate the select statement based on the current user's role
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    select_stmt: Select = notes_repo.query_list(client_report_id=client_report.id)
    response_out: Paginated[NoteRead] = (
        await permissions.get_paginated_resource_response(
            table_name=Note.__tablename__,
            stmt=select_stmt,
            page_params=PageParams(page=query.page, size=query.size),
            responses={
                RoleUser: NoteRead,
            },
        )
    )
    return response_out


@router.post(
    "/{client_id}/{report_id}/notes",
    name="client_report_notes:create",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
        Depends(get_client_or_404),
        Depends(get_client_report_or_404),
    ],
    response_model=NoteRead,
)
async def client_report_note_create(
    note_in: NoteCreate,
    client_report: ClientReport = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_report_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> NoteRead:
    """Creates a new note and assigns it to the client report.

    Permissions:
    ------------
    `role=admin|manager` : all client report notes

    `role=user` : only client report notes associated with the current user

    Returns:
    --------
    `NoteRead` : the client report note created

    """
    # verify current user has permission to take this action
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client_report.client_id,
    )
    # check note already exists
    notes_repo: NoteRepository = NoteRepository(session=permissions.db)
    a_note_title: Note | None = await notes_repo.read_by(
        field_name="title",
        field_value=note_in.title,
    )
    if a_note_title:
        raise NoteAlreadyExists()
    # create note
    new_note: Note = await notes_repo.create(note_in)
    # assign note to client report
    report_note_repo = ClientReportNoteRepository(session=permissions.db)
    await report_note_repo.create(
        ClientReportNoteCreate(client_report_id=client_report.id, note_id=new_note.id)
    )
    # return role based response
    response_out: NoteRead = permissions.get_resource_response(
        resource=new_note,
        responses={
            RoleUser: NoteRead,
        },
    )
    return response_out
