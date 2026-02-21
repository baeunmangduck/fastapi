import secrets

secret_keys = secrets.token_hex(32)
print(f"secret key: {secret_keys}")
