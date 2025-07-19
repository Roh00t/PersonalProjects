# CSCI368 Network Security - Assignment 1
# Student ID: 84867599
# Student Name: Rohit Panda

import hashlib
from cryptography.hazmat.primitives.asymmetric import dh

# Generate Diffie-Hellman parameters (p, g)
params = dh.generate_parameters(generator=2, key_size=512)
p = params.parameter_numbers().p
g = params.parameter_numbers().g

# Get input of password from user
password = input("Enter the password: ")

# Hash the password using SHA-1 for use as a symmetric key
hashed_password = hashlib.sha1(password.encode()).hexdigest()

# Save the DH parameters and hashed password to Alice/secret.txt
with open("Alice/secret.txt", "w") as f:
    f.write(f"{p},{g},{hashed_password}\n")

print("Diffie-Hellman parameters and hashed password saved to Alice/secret.txt")
