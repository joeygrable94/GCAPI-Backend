from fastapi import APIRouter, Depends, Request, Response

from app.api.deps import (
    AESCBCEncrypt,
    CurrentUser,
    RSAEncrypt,
    get_aes_cbc_encryption,
    get_rsa_encryption,
)
from app.core.config import Settings, get_settings
from app.core.security import (
    CsrfProtect,
    CsrfToken,
    EncryptedMessage,
    PlainMessage,
    RSADecryptMessage,
    RSAEncryptMessage,
    auth,
)

router: APIRouter = APIRouter()


@router.get(
    "/csrf",
    name="public:csrf",
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
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens(settings.api.csrf_key)

    csrf_protect.set_csrf_cookie(signed_token, response)
    response.headers["X-CSRF-Token"] = csrf_token

    return CsrfToken(csrf_token=csrf_token)


@router.post(
    "/encrypt/rsa",
    name="public:encrypt_rsa",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_rsa_encryption),
    ],
)
async def rsa_encrypt_message(
    request: Request,
    current_user: CurrentUser,
    rsa: RSAEncrypt,
    input: RSAEncryptMessage,
) -> RSADecryptMessage:
    """Encrypts a message using the public key of the API."""
    encrypted_message = rsa.encrypt(input.message)
    return RSADecryptMessage(message=encrypted_message)


@router.post(
    "/decrypt/rsa",
    name="public:decrypt_rsa",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_rsa_encryption),
    ],
)
async def rsa_decrypt_message(
    request: Request,
    current_user: CurrentUser,
    rsa: RSAEncrypt,
    input: RSADecryptMessage,
) -> RSAEncryptMessage:
    """Decrypts a message using the private key of the API."""
    decrypted_message = rsa.decrypt(input.message)
    return RSAEncryptMessage(message=decrypted_message)


@router.post(
    "/encrypt/aes-cbc",
    name="public:encrypt_aes_cbc",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_aes_cbc_encryption),
    ],
)
async def aes_cbc_encrypt_message(
    request: Request,
    current_user: CurrentUser,
    aes: AESCBCEncrypt,
    input: PlainMessage,
) -> EncryptedMessage:
    """Encrypts a message using AES CBC mode."""
    encrypted_message = aes.encrypt(input.message)
    return EncryptedMessage(message=encrypted_message)


@router.post(
    "/decrypt/aes-cbc",
    name="public:decrypt_aes_cbc",
    dependencies=[
        Depends(auth.implicit_scheme),
        Depends(get_aes_cbc_encryption),
    ],
)
async def aes_cbc_decrypt_message(
    request: Request,
    current_user: CurrentUser,
    aes: AESCBCEncrypt,
    input: EncryptedMessage,
) -> PlainMessage:
    """Decrypts a message using AES CBC mode."""
    decrypted_message = aes.decrypt(input.message)
    return PlainMessage(message=decrypted_message)
