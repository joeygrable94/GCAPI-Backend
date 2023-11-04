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


class AESEncryptionError(CipherError):
    def __init__(self, message: str = "AES cipher error encrypting message"):
        super().__init__(message=message)


class AESDecryptionError(CipherError):
    def __init__(self, message: str = "AES cipher error decrypting message"):
        super().__init__(message=message)


class RSAEncryptionError(CipherError):
    def __init__(self, message: str = "RSA cipher error encrypting message"):
        super().__init__(message=message)


class RSADecryptionError(CipherError):
    def __init__(self, message: str = "RSA cipher error decrypting message"):
        super().__init__(message=message)
