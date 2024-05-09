import json
from typing import Tuple

from Crypto.PublicKey import RSA

from app.core.config import settings


def load_api_keys() -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    rsa_public_key = json.loads(settings.api.rsa_public_key, strict=False)
    rsa_private_key = json.loads(settings.api.rsa_private_key, strict=False)

    public_key = RSA.import_key(rsa_public_key["public_key"])
    private_key = RSA.import_key(rsa_private_key["private_key"])

    return public_key, private_key
