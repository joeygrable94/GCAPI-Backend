from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.security import SecureMessage


def get_secure_message_encryption(
    settings: Settings = Depends(get_settings),
) -> SecureMessage:  # pragma: no cover
    return SecureMessage(
        pass_key=settings.api.encryption_key,
        salt=settings.api.encryption_salt,
    )


SecureMessageEncryption = Annotated[
    SecureMessage, Depends(get_secure_message_encryption)
]
