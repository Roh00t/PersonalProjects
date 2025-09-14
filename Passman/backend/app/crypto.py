import os, secrets
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

MASTER_KEY_B64 = os.getenv("MASTER_KEY")
if not MASTER_KEY_B64:
    raise RuntimeError("MASTER_KEY is required")
MASTER_KEY = __import__("base64").urlsafe_b64decode(MASTER_KEY_B64)

def derive_user_key(user_salt: bytes) -> bytes:
    # Derive 32-byte key from MASTER_KEY + per-user salt via HKDF-SHA256
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=user_salt,
        info=b"passmanager-user-key",
    )
    return hkdf.derive(MASTER_KEY)

def encrypt_blob(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
    aes = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ct = aes.encrypt(nonce, plaintext, None)
    return nonce, ct

def decrypt_blob(nonce: bytes, ciphertext: bytes, key: bytes) -> bytes:
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None)
