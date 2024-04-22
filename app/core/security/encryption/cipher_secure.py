from base64 import urlsafe_b64decode, urlsafe_b64encode

from Crypto.Cipher import AES
from Crypto.Cipher._mode_cbc import CbcMode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad

from app.core import logger

from .exceptions import DecryptionError, EncryptionError, SignatureVerificationError
from .keys import load_api_keys


class SecureMessage:
    def __init__(self, pass_key: str, salt: str) -> None:
        self.block_size: int = AES.block_size
        self.aes_key: bytes = PBKDF2(pass_key, salt.encode("utf-8"), dkLen=32)
        self.public_key: RSA.RsaKey
        self.private_key: RSA.RsaKey
        self.public_key, self.private_key = load_api_keys()
        self.salt = salt

    def _serialize_value(self, value: bool | str | int) -> bytes:
        if isinstance(value, bool):
            return b"true" if value else b"false"
        elif isinstance(value, str):
            return value.encode("utf-8")
        elif isinstance(value, int):
            return str(value).encode("utf-8")
        else:
            raise TypeError("Unsupported data type for encryption")

    def _deserialize_value(
        self, serialized_value: bytes, data_type: type[bool] | type[str] | type[int]
    ) -> object:
        if data_type == bool:
            return serialized_value == b"true"
        elif data_type == str:
            return serialized_value.decode("utf-8")
        elif data_type == int:
            return int(serialized_value.decode("utf-8"))
        else:
            raise TypeError("Unsupported data type for decryption")

    def sign_and_encrypt(self, value: bool | str | int) -> str:
        try:
            serialized_value = self._serialize_value(value)
            # Sign the value
            signer = PKCS1_v1_5.new(self.private_key)
            digest = SHA256.new()
            digest.update(serialized_value)
            signature = signer.sign(digest)
            # Generate a random IV
            iv = get_random_bytes(16)
            # Encrypt the value and the signature
            cipher: CbcMode = AES.new(self.aes_key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(
                pad((serialized_value + signature), self.block_size)
            )
            return urlsafe_b64encode(iv + ciphertext).decode("utf-8")
        except Exception as e:
            logger.exception(e)
            raise EncryptionError()

    def decrypt_and_verify(
        self, ciphertext: str, data_type: type[bool] | type[str] | type[int]
    ) -> object:
        try:
            # Decode the ciphertext and extract the IV
            decoded = urlsafe_b64decode(ciphertext)
            iv, deciphertext = decoded[:16], decoded[16:]
            # Decrypt the value and the signature
            cipher: CbcMode = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(deciphertext), self.block_size)
            serialized_value, signature = plaintext[:-256], plaintext[-256:]
            # Verify the signature
            verifier = PKCS1_v1_5.new(self.public_key)
            digest = SHA256.new()
            digest.update(serialized_value)
            if verifier.verify(digest, signature):
                return self._deserialize_value(serialized_value, data_type)
            else:
                raise SignatureVerificationError()
        except SignatureVerificationError as e:
            raise SignatureVerificationError(message=e.message)
        except Exception as e:
            logger.exception(e)
            raise DecryptionError()
