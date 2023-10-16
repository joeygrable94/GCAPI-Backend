import os
from typing import Tuple

import rsa

from app.core.config import settings


def generate_api_keys(file_key: str = settings.api.key) -> None:
    (pub_key, pvt_key) = rsa.newkeys(512)
    private_pem = pub_key.save_pkcs1().decode()
    public_pem = pvt_key.save_pkcs1().decode()
    with open(f"./certs/{file_key}_private_key.pem", "w") as pr:
        pr.write(private_pem)
    with open(f"./certs/{file_key}_public_key.pem", "w") as pu:
        pu.write(public_pem)


def load_api_keys(
    file_key: str = settings.api.key,
) -> Tuple[rsa.PrivateKey, rsa.PublicKey]:
    pub_pem_file = f"{settings.api.root_dir}/{file_key}_private_key.pem"
    pvt_pem_file = f"{settings.api.root_dir}/{file_key}_public_key.pem"
    if not os.path.exists(pub_pem_file) and not os.path.exists(pvt_pem_file):
        generate_api_keys(settings.api.key)
        load_api_keys(settings.api.key)
    with open(pub_pem_file, "r") as pu:
        public_pem = pu.read().encode("utf-8")
    with open(pvt_pem_file, "r") as pr:
        private_pem = pr.read().encode("utf-8")
    pub_key = rsa.PublicKey.load_pkcs1(public_pem)
    pvt_key = rsa.PrivateKey.load_pkcs1(private_pem)
    return pvt_key, pub_key
