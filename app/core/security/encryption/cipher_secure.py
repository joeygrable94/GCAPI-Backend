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

    def sign_and_encrypt(self, message: str) -> str:
        try:
            # Sign the message
            signer = PKCS1_v1_5.new(self.private_key)
            digest = SHA256.new()
            digest.update(message.encode("utf-8"))
            signature = signer.sign(digest)
            # Generate a random IV
            iv = get_random_bytes(16)
            # Encrypt the message and the signature
            cipher: CbcMode = AES.new(self.aes_key, AES.MODE_CBC, iv)
            ciphertext = cipher.encrypt(
                pad((message.encode("utf-8") + signature), self.block_size)
            )
            return urlsafe_b64encode(iv + ciphertext).decode("utf-8")
        except Exception as e:
            logger.exception(e)
            raise EncryptionError()

    def decrypt_and_verify(self, ciphertext: str) -> str:
        try:
            # Decode the ciphertext and extract the IV
            decoded = urlsafe_b64decode(ciphertext)
            iv, deciphertext = decoded[:16], decoded[16:]
            # Decrypt the message and the signature
            cipher: CbcMode = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            plaintext = unpad(cipher.decrypt(deciphertext), self.block_size)
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
