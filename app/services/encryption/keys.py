import json

from Crypto.PublicKey import RSA

from .settings import encryption_settings


def load_api_keys() -> tuple[RSA.RsaKey, RSA.RsaKey]:
    rsa_public_key = json.loads(encryption_settings.rsa_public_key, strict=False)
    rsa_private_key = json.loads(encryption_settings.rsa_private_key, strict=False)

    public_key = RSA.import_key(rsa_public_key["public_key"])
    private_key = RSA.import_key(rsa_private_key["private_key"])

    return public_key, private_key
