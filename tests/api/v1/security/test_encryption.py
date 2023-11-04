"""
test_encrypt_message_with_rsa
test_decrypt_message_with_rsa
test_encrypt_message_with_rsa_too_long_message
test_encrypt_message_with_aes_cbc
test_dncrypt_message_with_aes_cbc

POST
await client.post(
    "/encrypt/rsa",
    json=RSAEncryptMessage(message="").model_dump()
)

POST
await client.post(
    "/decrypt/rsa",
    json=RSADecryptMessage(message="").model_dump()
)

test_encrypt_and_decrypt_message_with_aes_cbc

POST
await client.post(
    "/encrypt/aes-cbc",
    json=PlainMessage(message="").model_dump()
)

POST
await client.post(
    "/decrypt/aes-cbc",
    json=EncryptedMessage(message="").model_dump()
)
"""
