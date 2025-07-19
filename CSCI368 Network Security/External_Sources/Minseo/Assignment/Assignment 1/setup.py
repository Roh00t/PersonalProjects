# CSCI368 Network Security - Assignment 1
# Student ID: 8225746
# Student Name: Minseo Yun
# Date: 2024-08-01

import hashlib
from cryptography.hazmat.primitives.asymmetric import dh

params = dh.generate_parameters(generator=2, key_size=512)
p = params.parameter_numbers().p
g = params.parameter_numbers().g

# Get input of password
password = input("Enter the password: ")

hashed_password = hashlib.sha1(password.encode()).hexdigest()

with open("Alice/secret.txt", "w") as f:
    f.write(f"{p},{g},{hashed_password}\n")

print("Diffie-Hellman parameters and hashed password saved to Alice/secret.txt")
