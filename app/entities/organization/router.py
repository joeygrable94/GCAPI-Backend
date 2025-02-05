from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import Select

from app.api.get_query import CommonUserQueryParams, GetUserQueryParams
from app.core.pagination import PageParams, Paginated
from app.entities.api.dependencies import get_async_db
from app.entities.api.errors import EntityNotFound
from app.entities.auth.dependencies import (
    Permission,
    PermissionController,
    get_current_user,
    get_permission_controller,
)
from app.entities.organization.crud import OrganizationRepository
from app.entities.organization.dependencies import get_organization_or_404
from app.entities.organization.errors import (
    OrganizationAlreadyExists,
    OrganizationNotFound,
    OrganizationRelationshipNotFound,
)
from app.entities.organization.model import Organization
from app.entities.organization.schemas import (
    OrganizationCreate,
    OrganizationDelete,
    OrganizationRead,
    OrganizationReadPublic,
    OrganizationUpdate,
)
from app.entities.organization_platform.crud import OrganizationPlatformRepository
from app.entities.organization_platform.model import OrganizationPlatform
from app.entities.organization_platform.schemas import (
    OrganizationPlatformCreate,
    OrganizationPlatformRead,
)
from app.entities.organization_website.crud import OrganizationWebsiteRepository
from app.entities.organization_website.model import OrganizationWebsite
from app.entities.organization_website.schemas import (
    OrganizationWebsiteCreate,
    OrganizationWebsiteRead,
)
from app.entities.platform.crud import PlatformRepository
from app.entities.platform.model import Platform
from app.entities.user.crud import UserRepository
from app.entities.user.errors import UserNotFound
from app.entities.user.model import User
from app.entities.user_organization.crud import UserOrganizationRepository
from app.entities.user_organization.model import UserOrganization
from app.entities.user_organization.schemas import (
    UserOrganizationCreate,
    UserOrganizationRead,
)
from app.entities.website.crud import WebsiteRepository
from app.entities.website.model import Website
from app.services.permission import (
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
from app.tasks.background import bg_task_request_to_delete_organization

router: APIRouter = APIRouter()


@router.get(
    "/",
    name="organizations:list",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[OrganizationRead],
)
async def organizations_list(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[OrganizationRead]:
    """Retrieve a paginated list of organizations.

    Permissions:
    ------------
    `role=admin|manager` : all organizations

    `role=user` : only organizations associated with the user via `user_organization`
        table

    Returns:
    --------
    `Paginated[OrganizationRead]` : a paginated list of organizations, optionally filtered

    """
    select_stmt: Select
    if RoleAdmin in permissions.privileges or RoleManager in permissions.privileges:
        select_stmt = permissions.organization_repo.query_list(user_id=query.user_id)
    else:
        select_stmt = permissions.organization_repo.query_list(
            user_id=permissions.current_user.id
        )
    response_out: Paginated[
        OrganizationRead
    ] = await permissions.get_paginated_resource_response(
        table_name=Organization.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleAdmin: OrganizationRead,
            RoleManager: OrganizationRead,
            RoleClient: OrganizationRead,
            RoleEmployee: OrganizationRead,
        },
    )
    return response_out


@router.get(
    "/public",
    name="organizations:list_public",
    dependencies=[
        Depends(CommonUserQueryParams),
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=Paginated[OrganizationReadPublic],
)
async def organizations_list_public(
    query: GetUserQueryParams,
    permissions: PermissionController = Depends(get_permission_controller),
) -> Paginated[OrganizationReadPublic]:
    """Retrieve a paginated list of organizations.

    Permissions:
    ------------
    `role=user` : all active organizations, but only public column data

    Returns:
    --------
    `Paginated[OrganizationReadPublic]` : a paginated list of active organizations public data

    """
    select_stmt: Select
    select_stmt = permissions.organization_repo.query_list(is_active=True)
    response_out: Paginated[
        OrganizationReadPublic
    ] = await permissions.get_paginated_resource_response(
        table_name=Organization.__tablename__,
        stmt=select_stmt,
        page_params=PageParams(page=query.page, size=query.size),
        responses={
            RoleUser: OrganizationReadPublic,
        },
    )
    return response_out


@router.post(
    "/",
    name="organizations:create",
    dependencies=[
        Depends(get_async_db),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationRead,
)
async def organizations_create(
    bg_tasks: BackgroundTasks,
    organization_in: OrganizationCreate,
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationRead:
    """Create a new organization.

    Permissions:
    ------------
    `role=admin|manager` : create a new organization

    Returns:
    --------
    `OrganizationRead` : the newly created organization

    """

    await permissions.verify_user_can_access(privileges=[RoleAdmin, RoleManager])
    organizations_repo: OrganizationRepository = OrganizationRepository(
        session=permissions.db
    )
    data = organization_in.model_dump()
    check_slug: str | None = data.get("slug")
    check_title: str | None = data.get("title")
    a_organization: Organization | None = None
    if check_slug:
        a_organization = await organizations_repo.read_by(
            field_name="slug",
            field_value=check_slug,
        )
        if a_organization:
            raise OrganizationAlreadyExists()
    if check_title:
        a_organization = await organizations_repo.read_by(
            field_name="title",
            field_value=check_title,
        )
        if a_organization:
            raise OrganizationAlreadyExists()
    new_organization: Organization = await organizations_repo.create(organization_in)

    response_out: OrganizationRead = permissions.get_resource_response(
        resource=new_organization,
        responses={
            RoleUser: OrganizationRead,
        },
    )
    return response_out


@router.get(
    "/{organization_id}",
    name="organizations:read",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationRead,
)
async def organizations_read(
    organization: Organization = Permission(
        [AccessRead, AccessReadSelf, AccessReadRelated], get_organization_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationRead:
    """Retrieve a single organization by id.

    Permissions:
    ------------
    `role=admin|manager` : all organizations

    `role=user` : only organizations associated with the user via `user_organization`

    Returns:
    --------
    `OrganizationRead` : a organization matching the organization_id

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )

    response_out: OrganizationRead = permissions.get_resource_response(
        resource=organization,
        responses={
            RoleUser: OrganizationRead,
        },
    )
    return response_out


@router.patch(
    "/{organization_id}",
    name="organizations:update",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationRead,
)
async def organizations_update(
    organization_in: OrganizationUpdate,
    organization: Organization = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_organization_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationRead:
    """Update a organization by id.

    Permissions:
    ------------
    `role=admin|manager` : all organizations

    `role=user` : only organizations associated with the user via `user_organization`

    Returns:
    --------
    `OrganizationRead` : the updated organization

    """

    permissions.verify_input_schema_by_role(
        input_object=organization_in,
        schema_privileges={
            RoleUser: OrganizationUpdate,
        },
    )

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    organizations_repo: OrganizationRepository = OrganizationRepository(
        session=permissions.db
    )
    if organization_in.title is not None:
        a_organization: Organization | None = await organizations_repo.read_by(
            field_name="title", field_value=organization_in.title
        )
        if a_organization:
            raise OrganizationAlreadyExists()
    updated_organization: Organization | None = await organizations_repo.update(
        entry=organization, schema=organization_in
    )

    response_out: OrganizationRead = permissions.get_resource_response(
        resource=updated_organization if updated_organization else organization,
        responses={
            RoleUser: OrganizationRead,
        },
    )
    return response_out


'''
@router.patch(
    "/{organization_id}/style-guide",
    name="organizations:update_style_guide",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationReadPublic,
)
async def organizations_update_style_guide(
    organization_in: OrganizationUpdateStyleGuide,
    organization: Organization = Permission(
        [AccessUpdate, AccessUpdateSelf, AccessUpdateRelated], get_organization_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationReadPublic:
    """Update a organization by id.

    Permissions:
    ------------
    `role=admin|manager` : all organizations

    `role=user` : only organizations associated with the user via `user_organization`

    Returns:
    --------
    `OrganizationReadPublic` : the updated organization public data

    """
    
    permissions.verify_input_schema_by_role(
        input_object=organization_in,
        schema_privileges={
            RoleUser: OrganizationUpdateStyleGuide,
        },
    )
    
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    organizations_repo: OrganizationRepository = OrganizationRepository(session=permissions.db)
    updated_organization: Organization | None = await organizations_repo.update(
        entry=organization, schema=OrganizationUpdate(style_guide=organization_in.style_guide)
    )
    
    response_out: OrganizationReadPublic = permissions.get_resource_response(
        resource=updated_organization if updated_organization else organization,
        responses={
            RoleUser: OrganizationReadPublic,
        },
    )
    return response_out
'''


@router.delete(
    "/{organization_id}",
    name="organizations:delete",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationDelete,
)
async def organizations_delete(
    bg_tasks: BackgroundTasks,
    organization: Organization = Permission(
        [AccessDelete, AccessDeleteSelf], get_organization_or_404
    ),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationDelete:
    """Delete a organization by id.

    Permissions:
    ------------
    `role=admin` : all organizations

    `role=organization` : may request to have their organization data deleted

    Returns:
    --------
    `OrganizationDelete` : a message indicating the user deleted a organization or if a user
        requested to delete a organization they are associated with

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin], organization_id=organization.id
    )
    output_message: str
    if RoleAdmin in permissions.privileges:
        organizations_repo: OrganizationRepository = OrganizationRepository(
            session=permissions.db
        )
        await organizations_repo.delete(entry=organization)
        output_message = "Organization deleted"
    else:
        bg_tasks.add_task(
            bg_task_request_to_delete_organization,
            user_id=str(permissions.current_user.id),
            organization_id=str(organization.id),
        )
        output_message = "Organization requested to be deleted"
    return OrganizationDelete(
        message=output_message,
        user_id=permissions.current_user.id,
        organization_id=organization.id,
    )


# organization relationships


@router.post(
    "/{organization_id}/assign/user",
    name="organizations:assign_user",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserOrganizationRead,
)
async def organizations_assign_user(
    user_organization_in: UserOrganizationCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserOrganizationRead:
    """Assigns a user to a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `UserOrganizationRead` : the user organization relationship that was created

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    # check if organization and user exists
    if user_organization_in.organization_id != organization.id:
        raise OrganizationNotFound()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(
        entry_id=user_organization_in.user_id
    )
    if user_exists is None:
        raise UserNotFound()
    user_organization_repo: UserOrganizationRepository = UserOrganizationRepository(
        session=permissions.db
    )
    user_organization: (
        UserOrganization | None
    ) = await user_organization_repo.exists_by_fields(
        {
            "user_id": user_organization_in.user_id,
            "organization_id": user_organization_in.organization_id,
        }
    )
    if user_organization is None:
        user_organization = await user_organization_repo.create(
            schema=user_organization_in
        )
    return UserOrganizationRead.model_validate(user_organization)


@router.post(
    "/{organization_id}/remove/user",
    name="organizations:remove_user",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=UserOrganizationRead,
)
async def organizations_remove_user(
    user_organization_in: UserOrganizationCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> UserOrganizationRead:
    """Removes a user from a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `UserOrganizationRead` : the user organization relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    # check if organization and user exists
    if user_organization_in.organization_id != organization.id:
        raise OrganizationNotFound()
    user_repo: UserRepository = UserRepository(session=permissions.db)
    user_exists: User | None = await user_repo.read(
        entry_id=user_organization_in.user_id
    )
    if user_exists is None:
        raise UserNotFound()
    user_organization_repo: UserOrganizationRepository = UserOrganizationRepository(
        session=permissions.db
    )
    user_organization: (
        UserOrganization | None
    ) = await user_organization_repo.exists_by_fields(
        {
            "user_id": user_organization_in.user_id,
            "organization_id": user_organization_in.organization_id,
        }
    )
    if user_organization is None:
        raise OrganizationRelationshipNotFound()
    await user_organization_repo.delete(user_organization)
    return UserOrganizationRead.model_validate(user_organization)


@router.post(
    "/{organization_id}/assign/platform",
    name="organizations:assign_platform",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationPlatformRead,
)
async def organizations_assign_platform(
    organization_platform_in: OrganizationPlatformCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationPlatformRead:
    """Assigns a platform to a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `OrganizationPlatformRead` : the organization platform relationship that was created

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    if organization_platform_in.organization_id != organization.id:
        raise OrganizationNotFound()
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    platform_exists: Platform | None = await platform_repo.read(
        entry_id=organization_platform_in.platform_id
    )
    if platform_exists is None:
        raise EntityNotFound(
            entity_info="Platform id = {}".format(organization_platform_in.platform_id)
        )
    organization_platform_repo = OrganizationPlatformRepository(session=permissions.db)
    organization_platform: (
        OrganizationPlatform | None
    ) = await organization_platform_repo.exists_by_fields(
        {
            "organization_id": organization_platform_in.organization_id,
            "platform_id": organization_platform_in.platform_id,
        }
    )
    if organization_platform is None:
        organization_platform = await organization_platform_repo.create(
            schema=organization_platform_in
        )
    return OrganizationPlatformRead.model_validate(organization_platform)


@router.post(
    "/{organization_id}/remove/platform",
    name="organizations:remove_platform",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationPlatformRead,
)
async def organizations_remove_platform(
    organization_platform_in: OrganizationPlatformCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationPlatformRead:
    """Removes a platform from a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `OrganizationPlatformRead` : the organization platform relationship that was deleted

    """
    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        organization_id=organization.id,
    )
    if organization_platform_in.organization_id != organization.id:
        raise OrganizationNotFound()
    platform_repo: PlatformRepository = PlatformRepository(session=permissions.db)
    platform_exists: Platform | None = await platform_repo.read(
        entry_id=organization_platform_in.platform_id
    )
    if platform_exists is None:
        raise EntityNotFound(
            entity_info="Platform id = {}".format(organization_platform_in.platform_id)
        )
    organization_platform_repo = OrganizationPlatformRepository(session=permissions.db)
    organization_platform: (
        OrganizationPlatform | None
    ) = await organization_platform_repo.exists_by_fields(
        {
            "organization_id": organization_platform_in.organization_id,
            "platform_id": organization_platform_in.platform_id,
        }
    )
    if organization_platform is None:
        raise OrganizationRelationshipNotFound()
    await organization_platform_repo.delete(organization_platform)
    return OrganizationPlatformRead.model_validate(organization_platform)


@router.post(
    "/{organization_id}/assign/website",
    name="organizations:assign_website",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationWebsiteRead,
)
async def organizations_assign_website(
    organization_website_in: OrganizationWebsiteCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationWebsiteRead:
    """Assigns a website to a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `OrganizationWebsiteRead` : the organization website relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=organization_website_in.website_id,
    )
    # check if organization and user exists
    if organization_website_in.organization_id != organization.id:
        raise OrganizationNotFound()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=organization_website_in.website_id
    )
    if website_exists is None:
        raise EntityNotFound(
            entity_info="Website {}".format(organization_website_in.website_id)
        )
    organization_website_repo: OrganizationWebsiteRepository = (
        OrganizationWebsiteRepository(session=permissions.db)
    )
    organization_website: (
        OrganizationWebsite | None
    ) = await organization_website_repo.exists_by_fields(
        {
            "website_id": organization_website_in.website_id,
            "organization_id": organization_website_in.organization_id,
        }
    )
    if organization_website is None:
        organization_website = await organization_website_repo.create(
            schema=organization_website_in
        )
    return OrganizationWebsiteRead.model_validate(organization_website)


@router.post(
    "/{organization_id}/remove/website",
    name="organizations:remove_website",
    dependencies=[
        Depends(get_async_db),
        Depends(get_organization_or_404),
        Depends(get_current_user),
        Depends(get_permission_controller),
    ],
    response_model=OrganizationWebsiteRead,
)
async def organizations_remove_website(
    organization_website_in: OrganizationWebsiteCreate,
    organization: Organization = Permission([AccessUpdate], get_organization_or_404),
    permissions: PermissionController = Depends(get_permission_controller),
) -> OrganizationWebsiteRead:
    """Removes a website from a organization.

    Permissions:
    ------------
    `role=admin|manager` : ...

    Returns:
    --------
    `OrganizationWebsiteRead` : the organization website relationship that was deleted

    """

    await permissions.verify_user_can_access(
        privileges=[RoleAdmin, RoleManager],
        website_id=organization_website_in.website_id,
    )
    # check if organization and user exists
    if organization_website_in.organization_id != organization.id:
        raise OrganizationNotFound()
    website_repo: WebsiteRepository = WebsiteRepository(session=permissions.db)
    website_exists: Website | None = await website_repo.read(
        entry_id=organization_website_in.website_id
    )
    if website_exists is None:
        raise EntityNotFound(
            entity_info="Website {}".format(organization_website_in.website_id)
        )
    organization_website_repo: OrganizationWebsiteRepository = (
        OrganizationWebsiteRepository(session=permissions.db)
    )
    organization_website: (
        OrganizationWebsite | None
    ) = await organization_website_repo.exists_by_fields(
        {
            "website_id": organization_website_in.website_id,
            "organization_id": organization_website_in.organization_id,
        }
    )
    if organization_website is None:
        raise OrganizationRelationshipNotFound()
    await organization_website_repo.delete(organization_website)
    return OrganizationWebsiteRead.model_validate(organization_website)
