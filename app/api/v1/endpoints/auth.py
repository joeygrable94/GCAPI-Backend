from typing import Any, Optional, Tuple

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Response,
    status,
)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.api.errors import ErrorCode
from app.api.exceptions import InvalidPasswordException, UserAlreadyExists
from app.api.openapi import (
    auth_access_responses,
    auth_logout_responses,
    auth_password_forgot_responses,
    auth_password_reset_responses,
    auth_refresh_responses,
    auth_register_responses,
    auth_revoke_responses,
    auth_verification_confirmation_responses,
    auth_verification_responses,
)
from app.core.config import Settings, get_settings
from app.core.logger import logger
from app.core.utilities import (
    send_account_updated,
    send_email_confirmation,
    send_email_reset_password,
    send_email_verification,
)
from app.db.schemas import (
    BearerResponse,
    JWToken,
    RequestUserCreate,
    UserCreate,
    UserRead,
    UserAdmin,
    UserUpdate,
)
from app.db.tables import User
from app.security import (
    AuthManager,
    get_current_active_password_reset_user,
    get_current_active_refresh_user,
    get_current_user_access_token,
    get_current_user_by_email,
    get_current_user_for_verification,
    get_user_auth,
)

router: APIRouter = APIRouter()


@router.post(
    "/register",
    name="auth:register",
    dependencies=[Depends(get_user_auth)],
    responses=auth_register_responses,
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def auth_register(
    background_tasks: BackgroundTasks,
    user_create: RequestUserCreate,
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> UserRead:
    """
    Registers a new user, then creates an email verification token
    and sends the new user an email verification link to click.
    """
    try:
        # register user
        create_user_dict = user_create.dict()
        create_user_dict["is_superuser"] = False
        create_user_dict["is_active"] = True
        create_user_dict["is_verified"] = False
        created_user: User = await oauth.users.create(
            schema=UserCreate(**create_user_dict)
        )
        new_user: UserAdmin = UserAdmin.from_orm(
            created_user
        )  # pragma: no cover
        # create verification token
        verify_token: str
        verify_token_csrf: str
        verify_token, verify_token_csrf = await oauth.store_token(  # pragma: no cover
            user=new_user,
            audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
            expires=settings.VERIFY_USER_TOKEN_LIFETIME,
        )
        # email verification link
        background_tasks.add_task(  # pragma: no cover
            send_email_verification,
            email_to=new_user.email,
            username=new_user.email,
            token=verify_token,
            csrf=verify_token_csrf,
        )
        # debug
        if settings.DEBUG_MODE:  # pragma: no cover
            logger.info(f"User {new_user.id} was registered.")
            logger.info(f"Email verification code to {new_user.id}.")
        # return user
        return UserRead.from_orm(new_user)  # pragma: no cover
    except UserAlreadyExists:
        raise HTTPException(  # pragma: no cover
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_ALREADY_EXISTS,
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.USER_PASSWORD_INVALID,
                "reason": e.reason,
            },
        )


@router.post(
    "/verification",
    name="auth:verification",
    dependencies=[Depends(get_user_auth)],
    responses=auth_verification_responses,
    response_model=None,
    status_code=status.HTTP_202_ACCEPTED,
)
async def auth_verification(
    background_tasks: BackgroundTasks,
    user: UserAdmin = Depends(get_current_user_by_email),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> None:
    """
    Sends an email verification link to the requested email.
    """
    # create verify token
    v_tok: str
    v_tok_csrf: str
    v_tok, v_tok_csrf = await oauth.store_token(
        user=user,
        audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
        expires=settings.VERIFY_USER_TOKEN_LIFETIME,
    )
    # email verification link
    background_tasks.add_task(  # pragma: no cover
        send_email_verification,
        email_to=user.email,
        username=user.email,
        token=v_tok,
        csrf=v_tok_csrf,
    )
    # debug
    if settings.DEBUG_MODE:  # pragma: no cover
        logger.info(f"Verification requested for user {user.id}.")


@router.get(
    "/confirmation",
    name="auth:confirmation",
    dependencies=[Depends(get_user_auth)],
    responses=auth_verification_confirmation_responses,
    status_code=status.HTTP_300_MULTIPLE_CHOICES,
)
async def auth_confirmation(
    background_tasks: BackgroundTasks,
    confirm_user: User = Depends(get_current_user_for_verification),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Any:
    """
    Confirms if the supplied verification token for the user is valid,
    then updates the is_verified status for the user.
    """
    # check the token in the request
    verified_user: User = await oauth.users.update(
        entry=confirm_user, schema=UserUpdate(is_verified=True)
    )
    # send email confirmation user now verified
    background_tasks.add_task(  # pragma: no cover
        send_email_confirmation,
        email_to=verified_user.email,
        username=verified_user.email,
        password="••••••••••••",
    )
    # debug
    if settings.DEBUG_MODE:  # pragma: no cover
        logger.info(f"User {verified_user.id} was verified.")
    # redirect
    return RedirectResponse(  # pragma: no cover
        url=f"http://{settings.SERVER_NAME}",
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


@router.post(
    "/forgot-password",
    name="auth:forgot_password",
    dependencies=[Depends(get_user_auth)],
    responses=auth_password_forgot_responses,
    response_model=None,
    status_code=status.HTTP_200_OK,
)
async def auth_forgot_password(
    background_tasks: BackgroundTasks,
    user: UserAdmin = Depends(get_current_user_by_email),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> None:
    """
    Emails a forgot password reset token to the user by email.
    """
    # create reset password token
    r_p_tok: str
    r_p_tok_csrf: str
    r_p_tok, r_p_tok_csrf = await oauth.store_token(
        user=user,
        audience=[settings.RESET_PASSWORD_TOKEN_AUDIENCE],
        expires=settings.RESET_PASSWORD_TOKEN_LIFETIME,
    )
    # email password reset token
    background_tasks.add_task(  # pragma: no cover
        send_email_reset_password,
        email_to=user.email,
        username=user.email,
        token=r_p_tok,
        csrf=r_p_tok_csrf,
    )
    # debug
    if settings.DEBUG_MODE:  # pragma: no cover
        logger.info(f"User {user.id} forgot their password.")


@router.post(
    "/reset-password",
    name="auth:reset_password",
    dependencies=[Depends(get_user_auth)],
    responses=auth_password_reset_responses,
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
async def auth_reset_password(
    background_tasks: BackgroundTasks,
    password: str = Body(...),
    user_reset: User = Depends(get_current_active_password_reset_user),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> UserRead:
    """
    Updates the user password for the subject in the request token.
    """
    try:
        updated_user: User = await oauth.users.update(
            entry=user_reset, schema=UserUpdate(password=password)
        )
        user_updated: UserRead = UserRead.from_orm(updated_user)  # pragma: no cover
        # email confirmation user password updated
        background_tasks.add_task(  # pragma: no cover
            send_account_updated,
            email_to=user_updated.email,
            username=user_updated.email,
            password="••••••••",
        )
        if settings.DEBUG_MODE:  # pragma: no cover
            logger.info(f"User {user_updated.id} reset their password.")
        return user_updated  # pragma: no cover
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.USER_PASSWORD_INVALID,
                "reason": e.reason,
            },
        )


@router.post(
    "/access",
    name="auth:access",
    dependencies=[
        Depends(get_user_auth),
        Depends(get_settings),
    ],
    responses=auth_access_responses,
    response_model=BearerResponse,
    status_code=status.HTTP_200_OK,
)
async def auth_access(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> BearerResponse:
    """
    Authenticates the user and grants them an access and a refresh token.
    """
    user: Optional[UserAdmin] = await oauth.certify(credentials)
    if user is None:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.BAD_CREDENTIALS,
        )
    if not user.is_active:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    if settings.USERS_REQUIRE_VERIFICATION and not user.is_verified:  # pragma: no cover
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_VERIFIED,
        )
    # write token
    a_tok: str
    a_tok_csrf: str
    r_tok: str
    r_tok_csrf: str
    a_tok, a_tok_csrf = await oauth.store_token(  # pragma: no cover
        user=user,
        audience=[settings.ACCESS_TOKEN_AUDIENCE],
        expires=settings.ACCESS_TOKEN_LIFETIME,
        is_fresh=True,
    )
    r_tok, r_tok_csrf = await oauth.store_token(  # pragma: no cover
        user=user,
        audience=[settings.REFRESH_TOKEN_AUDIENCE],
        expires=settings.REFRESH_TOKEN_LIFETIME,
        is_refresh=True,
    )
    return await oauth.bearer.get_login_response(  # pragma: no cover
        access_token=a_tok,
        access_token_csrf=a_tok_csrf,
        refresh_token=r_tok,
        refresh_token_csrf=r_tok_csrf,
        response=response,
    )


@router.post(
    "/refresh",
    name="auth:refresh",
    dependencies=[
        Depends(get_current_active_refresh_user),
        Depends(get_user_auth),
        Depends(get_settings),
    ],
    response_model=BearerResponse,
    responses=auth_refresh_responses,
    status_code=status.HTTP_200_OK,
)
async def auth_refresh(
    response: Response,
    user_token: Tuple[UserAdmin, JWToken, str] = Depends(
        get_current_active_refresh_user
    ),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> BearerResponse:
    """
    Refreshes current user access token and refresh tokens.
    """
    user: UserAdmin
    token_data: JWToken
    token_str: str
    user, token_data, token_str = user_token
    # add used refresh token to denylist
    await oauth.destroy_token(token_jti=token_data.jti, delete=False)
    # rotate access and refresh tokens
    a_tok: str
    a_tok_csrf: str
    r_tok: str
    r_tok_csrf: str
    a_tok, a_tok_csrf = await oauth.store_token(  # pragma: no cover
        user=user,
        audience=[settings.ACCESS_TOKEN_AUDIENCE],
        expires=settings.ACCESS_TOKEN_LIFETIME,
        is_fresh=True,
    )
    r_tok, r_tok_csrf = await oauth.store_token(  # pragma: no cover
        user=user,
        audience=[settings.REFRESH_TOKEN_AUDIENCE],
        expires=settings.REFRESH_TOKEN_LIFETIME,
        is_refresh=True,
    )
    # return rotated access and refresh tokens
    return await oauth.bearer.get_login_response(  # pragma: no cover
        access_token=a_tok,
        access_token_csrf=a_tok_csrf,
        refresh_token=r_tok,
        refresh_token_csrf=r_tok_csrf,
        response=response,
    )


@router.delete(
    "/revoke",
    name="auth:revoke",
    dependencies=[
        Depends(get_current_user_access_token),
        Depends(get_user_auth),
    ],
    response_model=BearerResponse,
    responses=auth_revoke_responses,
    status_code=status.HTTP_200_OK,
)
async def auth_revoke(
    response: Response,
    user_token: Tuple[UserAdmin, JWToken, str] = Depends(
        get_current_user_access_token
    ),
    oauth: AuthManager = Depends(get_user_auth),
) -> BearerResponse:
    """
    Revokes current user access token by adding it to the denylist.
    """
    user: UserAdmin
    token_data: JWToken
    token_str: str
    user, token_data, token_str = user_token
    # invalidate the used access token
    await oauth.destroy_token(token_jti=token_data.jti, delete=False)
    # return an empty bearer response
    return await oauth.bearer.get_logout_response(response=response)  # pragma: no cover


@router.delete(
    "/logout",
    name="auth:logout",
    dependencies=[
        Depends(get_current_user_access_token),
        Depends(get_user_auth),
    ],
    response_model=BearerResponse,
    responses=auth_logout_responses,
    status_code=status.HTTP_200_OK,
)
async def auth_logout(
    response: Response,
    user_token: Tuple[UserAdmin, JWToken, str] = Depends(
        get_current_user_access_token
    ),
    oauth: AuthManager = Depends(get_user_auth),
) -> BearerResponse:
    """
    Logout the current active user by access token and invalidates token id.
    """
    user: UserAdmin
    token_data: JWToken
    token_str: str
    user, token_data, token_str = user_token
    # invalidate the used access token
    await oauth.destroy_token(token_jti=token_data.jti, delete=True)
    # return an empty bearer response
    return await oauth.bearer.get_logout_response(response=response)  # pragma: no cover
