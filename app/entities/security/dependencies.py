from typing import Annotated

from fastapi import Depends

from app.services.encryption import (
    EncryptionSettings,
    SecureMessage,
    get_encryption_settings,
)


def get_secure_message_encryption(
    settings: EncryptionSettings = Depends(get_encryption_settings),
) -> SecureMessage:  # pragma: no cover
    return SecureMessage(
        pass_key=settings.encryption_key,
        salt=settings.encryption_salt,
    )


SecureMessageEncryption = Annotated[
    SecureMessage, Depends(get_secure_message_encryption)
]
