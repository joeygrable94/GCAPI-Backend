import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode

from Crypto import Random
from Crypto.Cipher import AES

from .exceptions import AESDecryptionError, AESEncryptionError


class AESCipherCBC(object):
    def __init__(self, key: str) -> None:
        self.block_size = AES.block_size
        self.key = hashlib.sha256(key.encode("utf-8")).digest()

    def encrypt(self, plain_text: str) -> str:
        try:
            padded_text = self.__pad(plain_text)
            iv = Random.new().read(self.block_size)
            cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=iv)
            encrypted_text = cipher.encrypt(padded_text.encode("utf-8"))
            return urlsafe_b64encode(iv + encrypted_text).decode("utf-8")
        except Exception:
            raise AESEncryptionError()

    def decrypt(self, encrypted_text: str) -> str:
        try:
            decrypted_text = urlsafe_b64decode(encrypted_text)
            iv = decrypted_text[: self.block_size]
            cipher = AES.new(key=self.key, mode=AES.MODE_CBC, iv=iv)
            plain_text = cipher.decrypt(
                decrypted_text[self.block_size :]  # noqa: E203
            ).decode("utf-8")
            return self.__unpad(plain_text)
        except Exception:
            raise AESDecryptionError()

    def __pad(self, plain_text: str) -> str:
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        ascii_string = chr(number_of_bytes_to_pad)
        padding_str = number_of_bytes_to_pad * ascii_string
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text: str) -> str:
        last_character = plain_text[len(plain_text) - 1 :]  # noqa: E203
        return plain_text[: -ord(last_character)]
