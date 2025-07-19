# CSCI368 Network Security - Assignment 1
# Student ID: 8225746
# Student Name: Minseo Yun
# Date: 2024-08-01

import socket
import hashlib
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

with open("secret.txt", "r") as f:
    p, g, hashed_password = f.read().strip().split(",")
    p = int(p)
    g = int(g)

print("Loaded Diffie-Hellman parameters and hashed password")

host = "127.0.0.1"
port = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, port))
print("UDP socket created")

data, addr = sock.recvfrom(1024)
if data.decode() == "Bob":
    print("\n[B -> A] Received connection from Bob")

    # Get a random secret int
    random_a = int.from_bytes(secrets.token_bytes(16), "big")
    # Encrypt message using hashed_password as a key
    message = f"{p} {g} {pow(g, random_a, p)}"
    cipher = Cipher(algorithms.ARC4(bytes.fromhex(hashed_password)), mode=None)
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode())
    sock.sendto(ciphertext, addr)
    print("\n[A -> B] Sent Diffie-Hellman parameters and g^a mod p")
    print(f"\t<random_a: {random_a}>")
    print(f"\t-> p: {p}\n\t-> g: {g}\n\t-> g^a mod p: {pow(g, random_a, p)}")

    # Receive g^b mod p
    data, addr = sock.recvfrom(1024)
    cipher = Cipher(algorithms.ARC4(bytes.fromhex(hashed_password)), mode=None)
    decryptor = cipher.decryptor()
    g_b = int(decryptor.update(data).decode())
    print("\n[B -> A] Received g^b mod p")
    print(f"\t<- g^b mod p: {g_b}")

    # Compute shared key
    shared_key = hashlib.sha1(pow(g_b, random_a, p).to_bytes(256, "big")).hexdigest()
    print("\n== Shared key computed ==")
    print(f"\t<Shared key: {shared_key}>")

    # Generate nonce
    nonce_a = secrets.token_bytes(16).hex().encode()
    # Encrypt nonce using shared key
    cipher = Cipher(algorithms.ARC4(bytes.fromhex(shared_key)), mode=None)
    encryptor = cipher.encryptor()
    encrypted_nonce_a = encryptor.update(nonce_a)
    sock.sendto(encrypted_nonce_a, addr)
    print("\n[A -> B] Sent nonce a to Bob")
    print(f"\t-> Nonce a: {nonce_a}")

    # Receive nonce from Bob
    data, addr = sock.recvfrom(1024)
    decryptor = cipher.decryptor()
    nonce_a_plus_1_plus_nonce_b = decryptor.update(data)
    nonce_a_plus_1 = nonce_a_plus_1_plus_nonce_b[:32]
    nonce_b = nonce_a_plus_1_plus_nonce_b[32:]
    print("\n[B -> A] Received nonce a + 1 and nonce b from Bob")
    print(f"\t<- Nonce a + 1: {nonce_a_plus_1}\n\t<- Nonce b: {nonce_b}")

    if nonce_a_plus_1 == (int.from_bytes(nonce_a, "big") + 1).to_bytes(32, "big"):
        print("\nReceived nonce a + 1 from Bob is correct")
    else:
        print("Login Failed")
        sock.sendto(encryptor.update("Login Failed".encode()), addr)
        exit()

    # Encrypt nonce_b + 1 using shared key
    nonce_b_plus_1 = (int.from_bytes(nonce_b, "big") + 1).to_bytes(32, "big")
    encryptor = cipher.encryptor()
    encrypted_nonce_b_plus_1 = encryptor.update(nonce_b_plus_1)
    sock.sendto(encrypted_nonce_b_plus_1, addr)
    print("\n[A -> B] Sent nonce b + 1 to Bob")
    print(f"\t-> Nonce b + 1: {nonce_b_plus_1}")

    # Check handshake completion
    data, addr = sock.recvfrom(1024)
    if data.decode() == "Handshake Complete":
        print("\nHandshake Complete")
        print()
        print("Login Successful")
        print()
    else:
        print("Handshake failed")
        exit()

    # Communication loop
    while True:
        message = input("Alice: ")
        kmk = shared_key + message + shared_key
        hashed_message = hashlib.sha1(kmk.encode()).hexdigest()
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update((message + hashed_message).encode())
        sock.sendto(encrypted_message, addr)
        if message == "exit":
            break

        data, addr = sock.recvfrom(1024)
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(data).decode()
        received_message = decrypted_message[:-40]
        received_hash = decrypted_message[-40:]
        kmk = shared_key + received_message + shared_key
        if received_hash == hashlib.sha1(kmk.encode()).hexdigest():
            if received_message == "exit":
                break
            print(f"Bob: {received_message}")
        else:
            print("Message integrity check failed")

else:
    print("Received connection from unknown source")
    exit()

sock.close()
