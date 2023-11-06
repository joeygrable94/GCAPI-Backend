from fastapi import status


class CipherError(Exception):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        message: str = "Cipher encryption Error",
    ):
        self.status_code = status_code
        self.message = message


class SignatureVerificationError(CipherError):
    def __init__(self, message: str = "error signing the message securely"):
        super().__init__(message=message)


class EncryptionError(CipherError):
    def __init__(self, message: str = "error encrypting message"):
        super().__init__(message=message)


class DecryptionError(CipherError):
    def __init__(self, message: str = "error decrypting message"):
        super().__init__(message=message)
