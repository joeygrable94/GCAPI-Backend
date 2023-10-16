from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.security import AESCipherCBC, RSACipher


def get_rsa_encryption() -> RSACipher:
    return RSACipher()


RSAEncrypt = Annotated[RSACipher, Depends(get_rsa_encryption)]


def get_aes_cbc_encryption(
    settings: Settings = Depends(get_settings),
) -> AESCipherCBC:
    return AESCipherCBC(key=settings.api.secret_key)


AESCBCEncrypt = Annotated[AESCipherCBC, Depends(get_aes_cbc_encryption)]
