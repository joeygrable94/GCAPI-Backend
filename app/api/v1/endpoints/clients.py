from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import Select

from app.api.deps import (
    CommonUserQueryParams,
    GetUserQueryParams,
    Permission,
    PermissionController,
    get_async_db,
    get_client_or_404,
    get_current_user,
    get_permission_controller,
)
from app.api.exceptions import (
    ClientAlreadyExists,
    ClientNotFound,
    ClientRelationshipNotFound,
    EntityNotFound,
    UserNotFound,
)
from app.core.pagination import PageParams, Paginated
from app.core.security.permissions import (
    AccessDelete,
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
from app.crud import (
    ClientRepository,
    ClientWebsiteRepository,
    PlatformRepository,
    UserClientRepository,
    UserRepository,
    WebsiteRepository,
)
from app.crud.client_platform import ClientPlatformRepository
from app.models import Client, ClientWebsite, User, UserClient, Website
from app.models.client_platform import ClientPlatform
from app.models.platform import Platform
from app.schemas import (
    ClientCreate,
    ClientDelete,
    ClientPlatformCreate,
    ClientPlatformRead,
    ClientRead,
    ClientReadPublic,
    ClientUpdate,
    ClientWebsiteCreate,
    ClientWebsiteRead,
    UserClientCreate,
    UserClientRead,
)
from app.tasks import bg_task_request_to_delete_client

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="clients:list",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[ClientRead],
)
async def clients_list(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[ClientRead]:
    """Retrieve a paginated list of clients.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`
        table

    Returns:
    --------
    `Paginated[ClientRead]` : a paginated list of clients, optionally filtered

    """
    # formulate the select statement based on the current user's role
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = permissions.client_repo.query_list(user_id=query.user_id)
    else:
        select_stmt = permissions.client_repo.query_list(
            user_id=permissions.current_user.id
        )

    response_out: Paginated[
        ClientRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Client.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: ClientRead,
            RoleManager: ClientRead,
            RoleClient: ClientRead,
            RoleEmployee: ClientRead,
        },
    )
    return response_out


@router.get(
    "/public",
    name="clients:list_public",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[ClientReadPublic],
)
async def clients_list_public(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[ClientReadPublic]:
    """Retrieve a paginated list of clients.

    Permissions:
    ------------
    `role=user` : all active clients, but only public column data

    Returns:
    --------
    `Paginated[ClientReadPublic]` : a paginated list of active clients public data

    """
    select_stmt: Select
    select_stmt = permissions.client_repo.query_list(is_active=True)
    response_out: Paginated[
        ClientReadPublic
    ] = await permissions.get_paginated_resource_response(
        table_name=Client.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: ClientReadPublic,
        },
    )
    return response_out


@router.post(
    "/",
    name="clients:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_create(
    bg_tasks: BackgroundTasks,
    client_in: ClientCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Create a new client.

    Permissions:
    ------------
    `role=admin|manager` : create a new client

    Returns:
    --------
    `ClientRead` : the newly created client

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    clients_repo: ClientRepository = ClientRepository(session=permissions.db)
    data = client_in.model_dump()
    check_slug: str | None = data.get("slug")
    check_title: str | None = data.get("title")
    a_client: Client | None = None
    if check_slug:
        a_client = await clients_repo.read_by(
            field_name="slug",
            field_value=check_slug,
        )
        if a_client:
            raise ClientAlreadyExists()
    if check_title:
        a_client = await clients_repo.read_by(
            field_name="title",
            field_value=check_title,
        )
        if a_client:
            raise ClientAlreadyExists()
    new_client: Client = await clients_repo.create(client_in)

    response_out: ClientRead = permissions.get_resource_response(
        resource=new_client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.get(
    "/{client_id}",
    name="clients:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_read(
    client: Client = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Retrieve a single client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`

    Returns:
    --------
    `ClientRead` : a client matching the client_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )

    response_out: ClientRead = permissions.get_resource_response(
        resource=client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


@router.patch(
    "/{client_id}",
    name="clients:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientRead,
)
async def clients_update(
    client_in: ClientUpdate,
    client: Client = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientRead:
    """Update a client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`

    Returns:
    --------
    `ClientRead` : the updated client

    """

    permissions.verify_input_schema_by_role(
        input_object=client_in,
        schema_privileges={
            RoleUser: ClientUpdate,
        },
    )

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    clients_repo: ClientRepository = ClientRepository(session=permissions.db)
    if client_in.title is not None:
        a_client: Client | None = await clients_repo.read_by(
            field_name="title", field_value=client_in.title
        )
        if a_client:
            raise ClientAlreadyExists()
    updated_client: Client | None = await clients_repo.update(
        entry=client, schema=client_in
    )

    response_out: ClientRead = permissions.get_resource_response(
        resource=updated_client if updated_client else client,
        responses={
            RoleUser: ClientRead,
        },
    )
    return response_out


'''
@router.patch(
    "/{client_id}/style-guide",
    name="clients:update_style_guide",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientReadPublic,
)
async def clients_update_style_guide(
    client_in: ClientUpdateStyleGuide,
    client: Client = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_client_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientReadPublic:
    """Update a client by id.

    Permissions:
    ------------
    `role=admin|manager` : all clients

    `role=user` : only clients associated with the user via `user_client`

    Returns:
    --------
    `ClientReadPublic` : the updated client public data

    """
    
    permissions.verify_input_schema_by_role(
        input_object=client_in,
        schema_privileges={
            RoleUser: ClientUpdateStyleGuide,
        },
    )
    
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    clients_repo: ClientRepository = ClientRepository(session=permissions.db)
    updated_client: Client | None = await clients_repo.update(
        entry=client, schema=ClientUpdate(style_guide=client_in.style_guide)
    )
    
    response_out: ClientReadPublic = permissions.get_resource_response(
        resource=updated_client if updated_client else client,
        responses={
            RoleUser: ClientReadPublic,
        },
    )
    return response_out
'''


@router.delete(
    "/{client_id}",
    name="clients:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientDelete,
)
async def clients_delete(
    bg_tasks: BackgroundTasks,
    client: Client = Permission([AccessDelete, AccessDeleteSelf], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientDelete:
    """Delete a client by id.

    Permissions:
    ------------
    `role=admin` : all clients

    `role=client` : may request to have their client data deleted

    Returns:
    --------
    `ClientDelete` : a message indicating the user deleted a client or if a user
        requested to delete a client they are associated with

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin], client_id=client.id
    )
    output_message: str
    if RoleAdmin in permissions.privileges:
        clients_repo: ClientRepository = ClientRepository(session=permissions.db)
        await clients_repo.delete(entry=client)
        output_message = "Client deleted"
    else:
        bg_tasks.add_task(
            bg_task_request_to_delete_client,
            user_id=str(permissions.current_user.id),
            client_id=str(client.id),
        )
        output_message = "Client requested to be deleted"
    return ClientDelete(
        message=output_message,
        user_id=permissions.current_user.id,
        client_id=client.id,
    )


# client relationships


@router.post(
    "/{client_id}/assign/user",
    name="clients:assign_user",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserClientRead,
)
async def clients_assign_user(
    user_client_in: UserClientCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserClientRead:
    """Assigns a user to a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `UserClientRead` : the user client relationship that was created

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # check if client and user exists
    if user_client_in.client_id != client.id:
        raise ClientNotFound()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(entry_id=user_client_in.user_id)
    if user_exists is None:
        raise UserNotFound()
    user_client_repo: UserClientRepository = UserClientRepository(
        session=permissions.db
    )
    user_client: UserClient | None = await user_client_repo.exists_by_fields(
        {"user_id": user_client_in.user_id, "client_id": user_client_in.client_id}
    )
    if user_client is None:
        user_client = await user_client_repo.create(schema=user_client_in)
    return UserClientRead.model_validate(user_client)


@router.post(
    "/{client_id}/remove/user",
    name="clients:remove_user",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserClientRead,
)
async def clients_remove_user(
    user_client_in: UserClientCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserClientRead:
    """Removes a user from a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `UserClientRead` : the user client relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    # check if client and user exists
    if user_client_in.client_id != client.id:
        raise ClientNotFound()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(entry_id=user_client_in.user_id)
    if user_exists is None:
        raise UserNotFound()
    user_client_repo: UserClientRepository = UserClientRepository(
        session=permissions.db
    )
    user_client: UserClient | None = await user_client_repo.exists_by_fields(
        {"user_id": user_client_in.user_id, "client_id": user_client_in.client_id}
    )
    if user_client is None:
        raise ClientRelationshipNotFound()
    await user_client_repo.delete(user_client)
    return UserClientRead.model_validate(user_client)


@router.post(
    "/{client_id}/assign/platform",
    name="clients:assign_platform",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientPlatformRead,
)
async def clients_assign_platform(
    client_platform_in: ClientPlatformCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientPlatformRead:
    """Assigns a platform to a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientPlatformRead` : the client platform relationship that was created

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    if client_platform_in.client_id != client.id:
        raise ClientNotFound()
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    platform_exists: Platform | None = await platform_repo.read(
        entry_id=client_platform_in.platform_id
    )
    if platform_exists is None:
        raise EntityNotFound(
            entity_info="Platform id = {}".format(client_platform_in.platform_id)
        )
    client_platform_repo = ClientPlatformRepository(session=permissions.db)
    client_platform: (
        ClientPlatform | None
    ) = await client_platform_repo.exists_by_fields(
        {
            "client_id": client_platform_in.client_id,
            "platform_id": client_platform_in.platform_id,
        }
    )
    if client_platform is None:
        client_platform = await client_platform_repo.create(schema=client_platform_in)
    return ClientPlatformRead.model_validate(client_platform)


@router.post(
    "/{client_id}/remove/platform",
    name="clients:remove_platform",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientPlatformRead,
)
async def clients_remove_platform(
    client_platform_in: ClientPlatformCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientPlatformRead:
    """Removes a platform from a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientPlatformRead` : the client platform relationship that was deleted

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        client_id=client.id,
    )
    if client_platform_in.client_id != client.id:
        raise ClientNotFound()
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    platform_exists: Platform | None = await platform_repo.read(
        entry_id=client_platform_in.platform_id
    )
    if platform_exists is None:
        raise EntityNotFound(
            entity_info="Platform id = {}".format(client_platform_in.platform_id)
        )
    client_platform_repo = ClientPlatformRepository(session=permissions.db)
    client_platform: (
        ClientPlatform | None
    ) = await client_platform_repo.exists_by_fields(
        {
            "client_id": client_platform_in.client_id,
            "platform_id": client_platform_in.platform_id,
        }
    )
    if client_platform is None:
        raise ClientRelationshipNotFound()
    await client_platform_repo.delete(client_platform)
    return ClientPlatformRead.model_validate(client_platform)


@router.post(
    "/{client_id}/assign/website",
    name="clients:assign_website",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientWebsiteRead,
)
async def clients_assign_website(
    client_website_in: ClientWebsiteCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientWebsiteRead:
    """Assigns a website to a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientWebsiteRead` : the client website relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], website_id=client_website_in.website_id
    )
    # check if client and user exists
    if client_website_in.client_id != client.id:
        raise ClientNotFound()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=client_website_in.website_id
    )
    if website_exists is None:
        raise EntityNotFound(
            entity_info="Website {}".format(client_website_in.website_id)
        )
    client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
        session=permissions.db
    )
    client_website: ClientWebsite | None = await client_website_repo.exists_by_fields(
        {
            "website_id": client_website_in.website_id,
            "client_id": client_website_in.client_id,
        }
    )
    if client_website is None:
        client_website = await client_website_repo.create(schema=client_website_in)
    return ClientWebsiteRead.model_validate(client_website)


@router.post(
    "/{client_id}/remove/website",
    name="clients:remove_website",
    dependencies=[
        Depends(get_async_db),
        Depends(get_client_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=ClientWebsiteRead,
)
async def clients_remove_website(
    client_website_in: ClientWebsiteCreate,
    client: Client = Permission([AccessUpdate], get_client_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> ClientWebsiteRead:
    """Removes a website from a client.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `ClientWebsiteRead` : the client website relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager], website_id=client_website_in.website_id
    )
    # check if client and user exists
    if client_website_in.client_id != client.id:
        raise ClientNotFound()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=client_website_in.website_id
    )
    if website_exists is None:
        raise EntityNotFound(
            entity_info="Website {}".format(client_website_in.website_id)
        )
    client_website_repo: ClientWebsiteRepository = ClientWebsiteRepository(
        session=permissions.db
    )
    client_website: ClientWebsite | None = await client_website_repo.exists_by_fields(
        {
            "website_id": client_website_in.website_id,
            "client_id": client_website_in.client_id,
        }
    )
    if client_website is None:
        raise ClientRelationshipNotFound()
    await client_website_repo.delete(client_website)
    return ClientWebsiteRead.model_validate(client_website)
