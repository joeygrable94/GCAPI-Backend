from typing import Any

from fastapi import APIRouter, Depends, Request, Response, Security

from app.api.deps import (
    CurrentUser,
    SecureMessageEncryption,
    get_secure_message_encryption,
)
from app.core.config import Settings, get_settings
from app.core.security import (
    CsrfProtect,
    CsrfToken,
    EncryptedMessage,
    PlainMessage,
    auth,
)
from app.core.security.auth.auth0 import Auth0User

router: APIRouter = APIRouter()


@router.get(
    "/test-scope",
    name="secure:test_security_scope",
    dependencies=[
        Depends(auth.implicit_scheme),
    ],
)
async def check_test_token_scope(
    user: Auth0User = Security(auth.get_user, scopes=["access:test"])
) -> Any:
    return {"status": "ok"}


@router.get(
    "/csrf",
    name="secure:get_csrf",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(CsrfProtect),
        Depends(get_settings),
    ],
    response_model=CsrfToken,
)
async def get_csrf(
    response: Response,
    current_user: CurrentUser,
    csrf_protect: CsrfProtect = Depends(),
    settings: Settings = Depends(get_settings),
) -> CsrfToken:
    """Generates an secure CSRF token for the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the CSRF token for the API

    """
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens(
        settings.api.csrf_secret_key
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    csrf_protect.set_csrf_header(csrf_token, response)

    return CsrfToken(csrf_token=csrf_token)


@router.post(
    "/csrf",
    name="secure:check_csrf",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(CsrfProtect),
        Depends(get_settings),
    ],
    response_model=None,
)
async def check_csrf(
    request: Request,
    response: Response,
    current_user: CurrentUser,
    csrf_protect: CsrfProtect = Depends(),
    settings: Settings = Depends(get_settings),
) -> None:
    """Verifies an secure CSRF token for the API.

    Permissions:
    ------------
    anyone can access this endpoint

    Returns:
    --------
    `Dict[str, Any]` : a dictionary containing the CSRF token for the API

    """
    await csrf_protect.validate_csrf(
        request,
        secret_key=settings.api.csrf_secret_key,
        cookie_key=settings.api.csrf_name_key,
    )
    csrf_protect.unset_csrf_cookie(response)  # prevent token reuse
    csrf_protect.unset_csrf_header(response)  # prevent token reuse
    return None


@router.post(
    "/encrypt/message",
    name="secure:secure_encrypt_message",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_secure_message_encryption),
    ],
)
async def secure_encrypt_message(
    request: Request,
    current_user: CurrentUser,
    secure: SecureMessageEncryption,
    input: PlainMessage,
) -> EncryptedMessage:
    """Encrypts a message using AES signed by an RSA key."""
    encrypted_message = secure.sign_and_encrypt(input.message)
    return EncryptedMessage(message=encrypted_message)


@router.post(
    "/decrypt/message",
    name="secure:secure_decrypt_message",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_secure_message_encryption),
    ],
)
async def secure_decrypt_message(
    request: Request,
    current_user: CurrentUser,
    secure: SecureMessageEncryption,
    input: EncryptedMessage,
) -> PlainMessage:
    """Decrypts and verifies the RSA signature of a securely encrypted message."""
    decrypted_message = secure.decrypt_and_verify(input.message)
    return PlainMessage(message=decrypted_message)
