import os
from pathlib import Path

from Crypto.PublicKey import RSA

from app.core.config import settings
from app.core.security.encryption.keys import generate_api_keys
from app.core.security.encryption.keys import load_api_keys


def test_generate_api_keys(tmp_path: Path) -> None:
    settings.api.root_dir = tmp_path  # type: ignore
    file_key = "test_key"
    generate_api_keys(file_key=file_key)

    private_key_file = tmp_path / f"{file_key}_private_key.pem"
    public_key_file = tmp_path / f"{file_key}_public_key.pem"

    assert private_key_file.exists()
    assert public_key_file.exists()

    with open(private_key_file, "r") as pr:
        private_key = pr.read()
    with open(public_key_file, "r") as pu:
        public_key = pu.read()

    assert "BEGIN RSA PRIVATE KEY" in private_key
    assert "END RSA PRIVATE KEY" in private_key
    assert "BEGIN PUBLIC KEY" in public_key
    assert "END PUBLIC KEY" in public_key

    os.remove(private_key_file)
    os.remove(public_key_file)


def test_load_api_keys(tmp_path: Path) -> None:
    settings.api.root_dir = tmp_path  # type: ignore
    file_key = "test_key"
    generate_api_keys(file_key=file_key)

    public_key, private_key = load_api_keys(file_key=file_key)

    assert isinstance(public_key, RSA.RsaKey)
    assert isinstance(private_key, RSA.RsaKey)

    os.remove(f"{tmp_path}/{file_key}_private_key.pem")
    os.remove(f"{tmp_path}/{file_key}_public_key.pem")
