"""

FOR EXPERIMENTAL TESTS ONLY

--------------------------------------------

import pytest

from app.core.config import settings
from app.core.security.encryption import SecureMessage

pytestmark = pytest.mark.asyncio

async def test_sign_and_encrypt() -> None:
    sm = SecureMessage(settings.api.encryption_key, settings.api.encryption_salt)
    messages = [
        "a" * 1,
        "a" * 10,
        "a" * 100,
        "a" * 1000,
        "a" * 10000,
        "a" * 100000,
        "a" * 1000000,
        "a" * 10000000,
        "a" * 100000000,
        "a" * 1000000000
    ]

    for message in messages:
        encrypted = sm.sign_and_encrypt(message)
        ratio = len(encrypted) / len(message)
        print(f"Input Length: {len(message)}, Encrypted Length: {len(encrypted)}, Ratio: {ratio}")  # noqa: E501

    assert False




Input Length: 1, Encrypted Length: 384, Ratio: 384.0
Input Length: 10, Encrypted Length: 384, Ratio: 38.4
Input Length: 100, Encrypted Length: 512, Ratio: 5.12
Input Length: 1000, Encrypted Length: 1708, Ratio: 1.708
Input Length: 10000, Encrypted Length: 13720, Ratio: 1.372
Input Length: 100000, Encrypted Length: 133720, Ratio: 1.3372
Input Length: 1000000, Encrypted Length: 1333720, Ratio: 1.33372
Input Length: 10000000, Encrypted Length: 13333720, Ratio: 1.333372
Input Length: 100000000, Encrypted Length: 133333720, Ratio: 1.3333372
Input Length: 1000000000, Encrypted Length: 1333333720, Ratio: 1.33333372

--------------------------------------------

This pattern suggests that as the input length increases exponentially,
the ratio approaches a limit around 1.333333... This is likely due to
the overhead introduced by encryption, which remains relatively constant
regardless of the input size.

"""
