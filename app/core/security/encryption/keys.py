import os
from typing import Tuple

from Crypto.PublicKey import RSA

from app.core.config import settings


def generate_api_keys(file_key: str = settings.api.key) -> None:
    key = RSA.generate(2048)
    private_key = key.export_key().decode()
    public_key = key.publickey().export_key().decode()
    private_key_file = f"{settings.api.root_dir}/{file_key}_private_key.pem"
    public_key_file = f"{settings.api.root_dir}/{file_key}_public_key.pem"
    with open(private_key_file, "w") as pr:
        pr.write(private_key)
    with open(public_key_file, "w") as pu:
        pu.write(public_key)


def load_api_keys(file_key: str = settings.api.key) -> Tuple[RSA.RsaKey, RSA.RsaKey]:
    private_key_file = f"{settings.api.root_dir}/{file_key}_private_key.pem"
    public_key_file = f"{settings.api.root_dir}/{file_key}_public_key.pem"

    if not os.path.exists(public_key_file) and not os.path.exists(
        private_key_file
    ):  # pragma: no cover
        generate_api_keys(file_key)
        load_api_keys(file_key)

    with open(private_key_file, "r") as pr:
        private_key = RSA.import_key(pr.read())

    with open(public_key_file, "r") as pu:
        public_key = RSA.import_key(pu.read())

    return public_key, private_key
