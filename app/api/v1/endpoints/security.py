from typing import Any, Dict

from fastapi import APIRouter, Depends, Request, Response

from app.api.deps import (
    AESCBCEncrypt,
    RSAEncrypt,
    get_aes_cbc_encryption,
    get_rsa_encryption,
)
from app.core.config import Settings, get_settings
from app.core.security import CsrfProtect
from app.schemas import (
    CsrfToken,
    EncryptedMessage,
    PlainMessage,
    RSADecryptMessage,
    RSAEncryptMessage,
)

router: APIRouter = APIRouter()


@router.get(
    "/csrf",
    name="public:csrf",
    dependencies=[
        Depends(CsrfProtect),
        Depends(get_settings),
    ],
    response_model=CsrfToken,
)
async def get_csrf(
    response: Response,
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

    return CsrfToken(csrf_token=csrf_token)


@router.post(
    "/encrypt/rsa",
    name="public:encrypt_rsa",
    dependencies=[
        Depends(get_rsa_encryption),
    ],
)
async def rsa_encrypt_message(
    request: Request,
    rsa: RSAEncrypt,
    message: RSAEncryptMessage,
) -> Dict[str, Any]:
    """Encrypts a message using the public key of the API."""
    encrypted_message = rsa.encrypt(message.message)
    return {"message": encrypted_message}


@router.post(
    "/decrypt/rsa",
    name="public:decrypt_rsa",
    dependencies=[
        Depends(get_rsa_encryption),
    ],
)
async def rsa_decrypt_message(
    request: Request,
    rsa: RSAEncrypt,
    message: RSADecryptMessage,
) -> Dict[str, Any]:
    """Decrypts a message using the private key of the API."""
    decrypted_message = rsa.decrypt(message.message)
    return {"message": decrypted_message}


@router.post(
    "/encrypt/aes-cbc",
    name="public:encrypt_aes_cbc",
    dependencies=[
        Depends(get_aes_cbc_encryption),
    ],
)
async def aes_cbc_encrypt_message(
    request: Request,
    aes: AESCBCEncrypt,
    message: PlainMessage,
) -> Dict[str, Any]:
    """Encrypts a message using AES CBC mode."""
    encrypted_message = aes.encrypt(message.message)
    return {"message": encrypted_message}


@router.post(
    "/decrypt/aes-cbc",
    name="public:decrypt_aes_cbc",
    dependencies=[
        Depends(get_aes_cbc_encryption),
    ],
)
async def aes_cbc_decrypt_message(
    request: Request,
    aes: AESCBCEncrypt,
    message: EncryptedMessage,
) -> Dict[str, Any]:
    """Decrypts a message using AES CBC mode."""
    decrypted_message = aes.decrypt(message.message)
    return {"message": decrypted_message}
