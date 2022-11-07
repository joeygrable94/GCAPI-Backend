from typing import Optional, Tuple, Union

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.security import OAuth2PasswordRequestForm

from app.api.errors import ErrorCode
from app.api.exceptions import InvalidPasswordException, UserAlreadyExists
from app.api.openapi import (
    auth_access_responses,
    auth_logout_responses,
    auth_register_responses,
)
from app.core.config import Settings, get_settings
from app.core.logger import logger
from app.core.utilities import send_email_verification
from app.db.schemas import BearerResponse, JWToken, UserCreate, UserRead
from app.db.tables import User
from app.security import AuthManager, get_current_user_access_token, get_user_auth

router: APIRouter = APIRouter()


@router.post(
    "/register",
    name="auth:register",
    dependencies=[Depends(get_user_auth)],
    responses=auth_register_responses,
    response_model=Union[UserRead, None],
    status_code=status.HTTP_201_CREATED,
)
async def auth_register(
    request: Request,
    background_tasks: BackgroundTasks,
    user_create: UserCreate,
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Optional[UserRead]:
    """
    Registers a new user, then creates an email verification token
    and sends the new user an email verification link to click.
    """
    try:
        # register user
        created_user: User = await oauth.users.create(schema=user_create)
        new_user: UserRead = UserRead.from_orm(created_user)
        # create verification token
        verify_user_token: Tuple[
            Optional[str], Optional[str]
        ] = await oauth.store_token(
            user=new_user,
            audience=[settings.VERIFY_USER_TOKEN_AUDIENCE],
            expires=settings.VERIFY_USER_TOKEN_LIFETIME,
        )
        verify_token: Optional[str]
        verify_token_csrf: Optional[str]
        verify_token, verify_token_csrf = verify_user_token
        if verify_token and verify_token_csrf:
            # email verification link
            background_tasks.add_task(
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
        return new_user
    except UserAlreadyExists:
        raise HTTPException(
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
    "/access",
    name="auth:access",
    dependencies=[
        Depends(get_user_auth),
        Depends(get_settings),
    ],
    responses=auth_access_responses,
    response_model=Union[BearerResponse, None],
    status_code=status.HTTP_200_OK,
)
async def auth_access(
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    oauth: AuthManager = Depends(get_user_auth),
    settings: Settings = Depends(get_settings),
) -> Optional[BearerResponse]:
    """
    Authenticates the user and grants them an access and a refresh token.
    """
    user: Optional[User] = await oauth.certify(credentials)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.BAD_CREDENTIALS,
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.USER_NOT_ACTIVE,
        )
    if settings.USERS_REQUIRE_VERIFICATION and not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorCode.USER_NOT_VERIFIED,
        )
    # write token
    access_token_auth: Tuple[Optional[str], Optional[str]]
    refresh_token_auth: Tuple[Optional[str], Optional[str]]
    access_token_auth = await oauth.store_token(
        user=user,
        audience=[settings.ACCESS_TOKEN_AUDIENCE],
        expires=settings.ACCESS_TOKEN_LIFETIME,
        is_fresh=True,
    )
    refresh_token_auth = await oauth.store_token(
        user=user,
        audience=[settings.REFRESH_TOKEN_AUDIENCE],
        expires=settings.REFRESH_TOKEN_LIFETIME,
        is_refresh=True,
    )
    access_token: Optional[str]
    access_token_csrf: Optional[str]
    access_token, access_token_csrf = access_token_auth
    refresh_token: Optional[str]
    refresh_token_csrf: Optional[str]
    refresh_token, refresh_token_csrf = refresh_token_auth
    # Return Access and Refresh Tokens
    if access_token and refresh_token:
        return await oauth.bearer.get_login_response(
            access_token=access_token,
            access_token_csrf=access_token_csrf,
            refresh_token=refresh_token,
            refresh_token_csrf=refresh_token_csrf,
            response=response,
        )
    else:
        return await oauth.bearer.get_login_response(
            access_token="",
            access_token_csrf="",
            refresh_token="",
            refresh_token_csrf="",
            response=response,
        )


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
    user_token: Tuple[Optional[UserRead], Optional[str], Optional[JWToken]] = Depends(
        get_current_user_access_token
    ),
    oauth: AuthManager = Depends(get_user_auth),
) -> BearerResponse:
    """
    Logout the current active user by access token and invalidates token id.
    """
    user: Optional[UserRead]
    access_token: Optional[str]
    token_data: Optional[JWToken]
    user, access_token, token_data = user_token
    # invalidate the used access token
    if access_token and user and token_data:
        await oauth.destroy_token(token_jti=token_data.jti, delete=True)
    # return an empty bearer response
    return await oauth.bearer.get_logout_response(response=response)
