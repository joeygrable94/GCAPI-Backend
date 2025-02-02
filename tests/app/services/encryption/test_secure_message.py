from base64 import urlsafe_b64decode
from datetime import date

import pytest
from Crypto.PublicKey import RSA

from app.services.encryption import (
    DecryptionError,
    EncryptionError,
    SecureMessage,
    SignatureVerificationError,
    encryption_settings,
)
from tests.utils.utils import random_boolean

pytestmark = pytest.mark.asyncio


async def test_encrypt_secure_msg() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    assert sm.block_size == 16
    assert len(sm.aes_key) == 32
    assert type(sm.public_key) is RSA.RsaKey
    assert type(sm.private_key) is RSA.RsaKey


async def test_sign_and_encrypt() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    decrypted = sm.decrypt_and_verify(encrypted, str)
    assert decrypted == message


async def test_sign_and_encrypt_boolean() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = random_boolean()
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    decrypted = sm.decrypt_and_verify(encrypted, bool)
    assert decrypted == message


async def test_sign_and_encrypt_integer() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = 12345
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    decrypted = sm.decrypt_and_verify(encrypted, int)
    assert decrypted == message


async def test_sign_and_encrypt_unsupported() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = date.today()
    encrypted = sm.sign_and_encrypt(message.isoformat())
    assert encrypted != message
    with pytest.raises(DecryptionError):
        sm.decrypt_and_verify(encrypted, date)  # type: ignore


async def test_sign_and_encrypt_serialize_value_type_error() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = date.today()
    with pytest.raises(EncryptionError):
        sm.sign_and_encrypt(message)  # type: ignore


async def test_sign_and_encryp_encryption_error() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    sm.block_size = 12
    message = "Hello, world!"
    with pytest.raises(EncryptionError):
        sm.sign_and_encrypt(message)


async def test_sign_and_encryp_signature_verification_error() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    sm.public_key = RSA.generate(2048)
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    with pytest.raises(SignatureVerificationError):
        sm.decrypt_and_verify(encrypted, str)


async def test_sign_and_encryp_decryption_error() -> None:
    sm = SecureMessage(
        encryption_settings.encryption_key, encryption_settings.encryption_salt
    )
    sm_bad = SecureMessage("wrong_key", "wrong_salt")
    message = "Hello, world!"
    encrypted = sm.sign_and_encrypt(message)
    assert encrypted != message
    assert urlsafe_b64decode(encrypted.encode("utf-8")) != message.encode("utf-8")
    with pytest.raises(DecryptionError):
        sm_bad.decrypt_and_verify(encrypted, str)
