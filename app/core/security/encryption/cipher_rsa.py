import rsa

from app.core.config import settings

from .exceptions import RSADecryptionError, RSAEncryptionError
from .keys import load_api_keys


class RSACipher(object):
    def __init__(self, file_key: str = settings.api.key):
        self.file_key: str = file_key
        self.pub_key: rsa.PublicKey
        self.pvt_key: rsa.PrivateKey
        self.pub_key, self.pvt_key = load_api_keys(file_key)

    def encrypt(self, plain_text: str) -> str:
        try:
            encrypted_text = rsa.encrypt(plain_text.encode("utf-8"), self.pub_key)
            return encrypted_text.hex()
        except Exception:
            raise RSAEncryptionError()

    def decrypt(self, encrypted_text: str) -> str:
        try:
            decrypted_txt = rsa.decrypt(bytes.fromhex(encrypted_text), self.pvt_key)
            return decrypted_txt.decode("utf-8")
        except Exception:
            raise RSADecryptionError()
