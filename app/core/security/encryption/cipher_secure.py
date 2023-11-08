import hashlib
from base64 import urlsafe_b64decode, urlsafe_b64encode

from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad

from app.core import logger

from .exceptions import DecryptionError, EncryptionError, SignatureVerificationError
from .keys import load_api_keys


class SecureMessage:
    def __init__(self, aes_key: str) -> None:
        self.block_size: int = AES.block_size
        self.aes_key: bytes = hashlib.sha256(aes_key.encode("utf-8")).digest()
        self.public_key: RSA.RsaKey
        self.private_key: RSA.RsaKey
        self.public_key, self.private_key = load_api_keys()

    def sign_and_encrypt(self, message: str) -> str:
        try:
            # Sign the message
            signer = PKCS1_v1_5.new(self.private_key)
            digest = SHA256.new()
            digest.update(message.encode("utf-8"))
            signature = signer.sign(digest)
            # Encrypt the message and the signature
            cipher: EcbMode = AES.new(self.aes_key, AES.MODE_ECB)
            ciphertext = cipher.encrypt(
                pad((message.encode("utf-8") + signature), self.block_size)
            )
            return urlsafe_b64encode(ciphertext).decode("utf-8")
        except Exception as e:
            logger.exception(e)
            raise EncryptionError()

    def decrypt_and_verify(self, ciphertext: str) -> str:
        try:
            # Decrypt the message and the signature
            cipher: EcbMode = AES.new(self.aes_key, AES.MODE_ECB)
            plaintext = unpad(
                cipher.decrypt(urlsafe_b64decode(ciphertext)), self.block_size
            )
            message, signature = plaintext[:-256], plaintext[-256:]
            # Verify the signature
            verifier = PKCS1_v1_5.new(self.public_key)
            digest = SHA256.new()
            digest.update(message)
            if verifier.verify(digest, signature):
                return message.decode("utf-8")
            else:
                raise SignatureVerificationError()
        except SignatureVerificationError as e:
            raise SignatureVerificationError(message=e.message)
        except Exception as e:
            logger.exception(e)
            raise DecryptionError()
