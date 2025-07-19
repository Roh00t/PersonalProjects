# CSCI368 Network Security - Assignment 1
# Student ID: 84867599
# Student Name: Rohit Panda


import socket
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

# Ask user for password and hash it for use as a key
password = input("Enter the password: ")
hashed_pw = hashlib.sha1(password.encode()).hexdigest()

# Setup UDP socket and send initial connection message to Alice
host = "127.0.0.1"
port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b"Bob", (host, port))
print("UDP socket created")

# Receive encrypted DH parameters and Alice's public value
data, addr = sock.recvfrom(1024)
cipher = Cipher(algorithms.ARC4(bytes.fromhex(hashed_pw)), mode=None)
decryptor = cipher.decryptor()
message = decryptor.update(data).decode()
p, g, g_a = map(int, message.split())
print("\n[A -> B] Received Diffie-Hellman parameters and public key")
print(f"\t<- p: {p}\n\t<- g: {g}\n\t<- g^a mod p: {g_a}")

# Generate Bob's random secret (private key) and send public value to Alice
random_b = int.from_bytes(secrets.token_bytes(16), "big")

cipher = Cipher(algorithms.ARC4(bytes.fromhex(hashed_pw)), mode=None)
encryptor = cipher.encryptor()
encrypted_message = encryptor.update(str(pow(g, random_b, p)).encode())
sock.sendto(encrypted_message, addr)
print("\n[B -> A] Sent g^b mod p to Alice")
print(f"\t<random_b: {random_b}>")
print(f"\t-> g^b mod p: {pow(g, random_b, p)}")

# Compute shared key using DH exchange and hash it
shared_key = hashlib.sha1(pow(g_a, random_b, p).to_bytes(256, "big")).hexdigest()
print("\n== Shared key computed ==")
print(f"\t<Shared key: {shared_key}>")

# Receive encrypted nonce from Alice using shared key
data, addr = sock.recvfrom(1024)
cipher = Cipher(algorithms.ARC4(bytes.fromhex(shared_key)), mode=None)
decryptor = cipher.decryptor()
nonce_a = decryptor.update(data)
print("\n[A -> B] Received nonce a from Alice")
print(f"\t<- Nonce a: {nonce_a}")

# Generate Bob's nonce, increment Alice's nonce, and send both to Alice (encrypted)
nonce_b = secrets.token_bytes(16).hex().encode()
nonce_a_plus_1 = (int.from_bytes(nonce_a, "big") + 1).to_bytes(32, "big")
message = nonce_a_plus_1 + nonce_b
encryptor = cipher.encryptor()
encrypted_nonce = encryptor.update(message)
sock.sendto(encrypted_nonce, addr)
print("\n[B -> A] Sent nonce a + 1 and nonce b to Alice")
print(f"\t-> Nonce a + 1: {nonce_a_plus_1}\n\t-> Nonce b: {nonce_b}")

# Receive encrypted nonce_b+1 from Alice and check for login failure
data, addr = sock.recvfrom(1024)
decryptor = cipher.decryptor()
nonce_b_plus_1 = decryptor.update(data)
if nonce_b_plus_1 == "Login Failed".encode():
    print("Login Failed")
    exit()
print("\n[A -> B] Received nonce b + 1 from Alice")
print(f"\t<- Nonce b + 1: {nonce_b_plus_1}")

# Verify Alice incremented nonce_b correctly, complete handshake if so
if nonce_b_plus_1 == (int.from_bytes(nonce_b, "big") + 1).to_bytes(32, "big"):
    print("\nReceived nonce b + 1 from Alice is correct")
    sock.sendto("Handshake Complete".encode(), addr)
    print("\nHandshake Complete")
    print()
    print("Login Successful")
    print()
else:
    print("Login Failed")
    exit()

# Communication loop for secure message exchange
while True:
    # Receive and decrypt message from Alice, verify integrity
    data, addr = sock.recvfrom(1024)
    decryptor = cipher.decryptor()
    message = decryptor.update(data).decode()
    received_hash = message[-40:]
    received_message = message[:-40]
    kmk = shared_key + received_message + shared_key
    if received_hash == hashlib.sha1(kmk.encode()).hexdigest():
        if received_message == "exit":
            break
        print(f"Alice: {received_message}")
    else:
        print("Message integrity check failed")

    # Encrypt and send message to Alice with hash for integrity
    message = input("Bob: ")
    kmk = shared_key + message + shared_key
    hashed_message = hashlib.sha1(kmk.encode()).hexdigest()
    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update((message + hashed_message).encode())
    sock.sendto(encrypted_message, addr)
    if message == "exit":
        break

sock.close()
