import hashlib
import json
from base64 import urlsafe_b64decode, urlsafe_b64encode

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from .exceptions import (
    AESDecryptionError,
    AESEncryptionError,
    SignatureVerificationError,
)


class SecureMessage:
    def __init__(self, key: str) -> None:
        self.block_size = AES.block_size
        self.aes_key = hashlib.sha256(key.encode("utf-8")).digest()
        self.rsa_key = RSA.generate(2048)  # Generate an RSA key pair

    def sign_and_encrypt(self, message: str) -> str:
        # Sign the message
        signer = PKCS1_v1_5.new(self.rsa_key)
        signature = signer.sign(hashlib.sha256(message.encode("utf-8")))

        # Encrypt the message and signature
        try:
            message_data = json.dumps(
                {
                    "message": message,
                    "signature": urlsafe_b64encode(signature).decode("utf-8"),
                }
            )
            padded_text = self.__pad(message_data)
            iv = Random.new().read(self.block_size)
            cipher = AES.new(key=self.aes_key, mode=AES.MODE_CBC, iv=iv)
            encrypted_text = cipher.encrypt(padded_text.encode("utf-8"))
            return urlsafe_b64encode(iv + encrypted_text).decode("utf-8")
        except ValueError:
            raise AESEncryptionError()

    def decrypt_and_verify(self, encrypted_message: str) -> str:
        try:
            decrypted_text = urlsafe_b64decode(encrypted_message)
            iv = decrypted_text[: self.block_size]  # noqa: E203
            cipher = AES.new(key=self.aes_key, mode=AES.MODE_CBC, iv=iv)
            decrypt_key = decrypted_text[self.block_size :]  # noqa: E203
            message_data = cipher.decrypt(decrypt_key).decode("utf-8")
            data = json.loads(self.__unpad(message_data))
            message = data.get("message", "").encode("utf-8")

            # Verify the signature
            signature = urlsafe_b64decode(data["signature"])
            verifier = PKCS1_v1_5.new(self.rsa_key)
            if verifier.verify(msg_hash=hashlib.sha256(message), signature=signature):
                return data["message"]
            else:
                raise SignatureVerificationError()
        except ValueError:
            raise AESDecryptionError()

    def __pad(self, plain_text: str) -> str:
        number_of_bytes_to_pad = self.block_size - len(plain_text) % self.block_size
        padding_str = chr(number_of_bytes_to_pad) * number_of_bytes_to_pad
        padded_plain_text = plain_text + padding_str
        return padded_plain_text

    @staticmethod
    def __unpad(plain_text: str) -> str:
        last_character = plain_text[-1]
        return plain_text[: -ord(last_character)]
