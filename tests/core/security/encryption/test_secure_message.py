from base64 import urlsafe_b64decode

import pytest
from Crypto.PublicKey import RSA

from app.core.config import settings
from app.core.security.encryption import DecryptionError
from app.core.security.encryption import EncryptionError
from app.core.security.encryption import SecureMessage
from app.core.security.encryption.exceptions import SignatureVerificationError

pytestmark = pytest.mark.asyncio


async def test_encrypt_secure_msg() -> None:
    sm = SecureMessage(settings.api.encryption_key)
    assert sm.block_size == 16
    assert len(sm.aes_key) == 32
    assert type(sm.public_key) is RSA.RsaKey
    assert type(sm.private_key) is RSA.RsaKey


async def test_sign_and_encrypt() -> None:
    sm = SecureMessage(settings.api.encryption_key)
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    decrypted = sm.decrypt_and_verify(encrypted)
    assert decrypted == message


async def test_sign_and_encryp_encryption_error() -> None:
    sm = SecureMessage(settings.api.encryption_key)
    sm.block_size = 12
    message = "Hello, world!"
    with pytest.raises(EncryptionError):
        sm.sign_and_encrypt(message)


async def test_sign_and_encryp_signature_verification_error() -> None:
    sm = SecureMessage(settings.api.encryption_key)
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    sm.public_key = RSA.generate(2048)
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    with pytest.raises(SignatureVerificationError):
        sm.decrypt_and_verify(encrypted)


async def test_sign_and_encryp_decryption_error() -> None:
    sm = SecureMessage(settings.api.encryption_key)
    sm_bad = SecureMessage("wrong_key")
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    with pytest.raises(DecryptionError):
        sm_bad.decrypt_and_verify(encrypted)
