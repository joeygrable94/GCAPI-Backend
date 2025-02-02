from Crypto.PublicKey import RSA

from app.services.encryption import load_api_keys


def test_load_api_keys() -> None:
    public_key, private_key = load_api_keys()

    assert isinstance(public_key, RSA.RsaKey)
    assert isinstance(private_key, RSA.RsaKey)
