# encryptor.py Core implementation of encryption algorithms 
from Crypto.Cipher import AES, DES3, ARC4, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA, ECC
from Crypto.Signature import DSS, pkcs1_15
from Crypto.Hash import SHA256
from twofish import Twofish
import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # More precise than time.time()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Execution Time: {(end - start)*1000:.3f} ms")  # Convert to milliseconds
        return result
    return wrapper

@measure_time
def twofish_encrypt_decrypt(data, password):
    print("\n=== Twofish Encryption/Decryption ===")
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode(), salt, dkLen=32, count=100000)
    
    tf = Twofish(key)
    block_size = 16
    padding_length = block_size - (len(data) % block_size)
    padded_data = data + bytes([padding_length] * padding_length)

    # Encrypt
    ciphertext = b''
    for i in range(0, len(padded_data), block_size):
        block = padded_data[i:i + block_size]
        ciphertext += tf.encrypt(block)
    print(f"Ciphertext (Twofish): {ciphertext.hex()}")  # Use hex for readability

    # Decrypt
    decrypted = b''
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        decrypted += tf.decrypt(block)
    
    decrypted = decrypted[:-decrypted[-1]]  # Remove padding
    print(f"Decrypted Text (Twofish): {decrypted.decode()}")
    return ciphertext, decrypted

@measure_time
def aes_encrypt_decrypt(data, password):
    print("\n=== AES-256-GCM Encryption/Decryption ===")
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode(), salt, dkLen=32, count=100000)
    cipher = AES.new(key, AES.MODE_GCM)
    
    ciphertext, tag = cipher.encrypt_and_digest(data)
    print(f"Ciphertext (AES): {ciphertext.hex()}")  # Use hex for readability

    # Decrypt
    cipher = AES.new(key, AES.MODE_GCM, nonce=cipher.nonce)
    try:
        decrypted = cipher.decrypt_and_verify(ciphertext, tag)
        print(f"Decrypted Text (AES): {decrypted.decode()}")
    except ValueError:
        print("Authentication failed! Data may be corrupted.")
    return ciphertext, decrypted

@measure_time
def des3_encrypt_decrypt(data, password):
    print("\n=== Triple DES Encryption/Decryption ===")
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode(), salt, dkLen=24, count=100000)
    cipher = DES3.new(key, DES3.MODE_EAX)
    
    ciphertext = cipher.encrypt(data)
    print(f"Ciphertext (3DES): {ciphertext.hex()}")  # Use hex for readability

    # Decrypt
    cipher = DES3.new(key, DES3.MODE_EAX, nonce=cipher.nonce)
    decrypted = cipher.decrypt(ciphertext)
    print(f"Decrypted Text (3DES): {decrypted.decode()}")
    return ciphertext, decrypted

@measure_time
def rc4_encrypt_decrypt(data, password):
    print("\n=== RC4 Encryption/Decryption ===")
    salt = get_random_bytes(16)
    key = PBKDF2(password.encode(), salt, dkLen=16, count=100000)
    cipher = ARC4.new(key)
    
    ciphertext = cipher.encrypt(data)
    print(f"Ciphertext (RC4): {ciphertext.hex()}")  # Use hex for readability

    # Decrypt
    cipher = ARC4.new(key)
    decrypted = cipher.decrypt(ciphertext)
    print(f"Decrypted Text (RC4): {decrypted.decode()}")
    return ciphertext, decrypted

@measure_time
def ecc_sign_verify(data):
    print("\n=== ECC Digital Signature ===")
    private_key = ECC.generate(curve='P-256')
    public_key = private_key.public_key()

    # Sign
    h = SHA256.new(data)
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(h)
    print(f"Digital Signature (ECC): {signature.hex()}")  # Use hex for readability

    # Verify
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("ECC Signature Verified Successfully!")
    except ValueError:
        print("ECC Signature Verification Failed!")
    return signature

@measure_time
def rsa_encrypt_sign(data):
    print("\n=== RSA-2048 Encryption/Decryption & Signature ===")
    # Generate key pair
    key = RSA.generate(2048)
    public_key = key.public_key()

    # Encrypt
    cipher_rsa = PKCS1_OAEP.new(public_key)
    session_key = get_random_bytes(16)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Use session key with AES
    cipher_aes = AES.new(session_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(data)

    print(f"Encrypted Session Key (RSA): {enc_session_key.hex()}")
    print(f"Ciphertext (Hybrid RSA-AES): {ciphertext.hex()}")

    # Sign
    hash_obj = SHA256.new(data)
    signature = pkcs1_15.new(key).sign(hash_obj)
    print(f"Digital Signature (RSA): {signature.hex()}")

    # Decrypt
    cipher_rsa = PKCS1_OAEP.new(key)
    dec_session_key = cipher_rsa.decrypt(enc_session_key)
    cipher_aes = AES.new(dec_session_key, AES.MODE_GCM, nonce=cipher_aes.nonce)
    decrypted = cipher_aes.decrypt_and_verify(ciphertext, tag)
    print(f"Decrypted Text (RSA): {decrypted.decode()}")

    # Verify signature
    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature)
        print("RSA Signature Verified Successfully!")
    except (ValueError, TypeError):
        print("RSA Signature Verification Failed!")
    
    return ciphertext, decrypted, signature