"""

------------------------------------------------------------

         1  ->  384         =  384.0
        10  ->  384         =  38.4
       100  ->  512         =  5.12
      1000  ->  1708        =  1.708
     10000  ->  13720       =  1.372
    100000  ->  133720      =  1.3372
   1000000  ->  1333720     =  1.33372
  10000000  ->  13333720    =  1.333372
 100000000  ->  133333720   =  1.3333372
1000000000  ->  1333333720  =  1.33333372

------------------------------------------------------------

        4   ->  384         = 96.0
       12   ->  384         = 32.0
       16   ->  408         = 25.5
       32   ->  428         = 13.375
       40   ->  428         = 10.7
       64   ->  472         = 7.375
       96   ->  512         = 5.333333333333333
      100   ->  512         = 5.12
      150   ->  576         = 3.84
      255   ->  704         = 2.76078431372549
      320   ->  812         = 2.5375
     1024   ->  1752        = 1.7109375
     2048   ->  3116        = 1.521484375
     5000   ->  7040        = 1.408
    65535   ->  87744       = 1.3388876173037307

------------------------------------------------------------


import pytest

from app.core.config import settings
from app.core.security.encryption import SecureMessage

pytestmark = pytest.mark.asyncio


async def test_sign_and_encrypt() -> None:
    sm = SecureMessage(settings.api.encryption_key, settings.api.encryption_salt)
    messages = [
        "a" * 4,
        "a" * 12,
        "a" * 16,
        "a" * 32,
        "a" * 40,
        "a" * 64,
        "a" * 96,
        "a" * 100,
        "a" * 150,
        "a" * 255,
        "a" * 320,
        "a" * 1024,
        "a" * 2048,
        "a" * 5000,
        "a" * 65535,
    ]

    for message in messages:
        encrypted = sm.sign_and_encrypt(message)
        ratio = len(encrypted) / len(message)
        print(f"Input Length: {len(message)}, Encrypted Length: {len(encrypted)}, Ratio: {ratio}")  # noqa: E501

    assert False

"""
