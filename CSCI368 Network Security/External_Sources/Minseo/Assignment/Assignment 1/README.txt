CSCI368 Network Security - Assignment 1
Student ID : 8225746
Student Name : Minseo Yun
Date : 2024-08-01

1. Environment

Developed & Tested OS : macOS 14.5 Sonoma
Used python version : Python 3.11.9 64-bit


2. Used libraries

2.1. Default Libraries

socket - Used for establishing UDP socket connection
hashlib - Used for SHA1 hashing
secrets - Used for generating secured pseudorandom numbers

2.2. External Libraries

https://pypi.org/project/cryptography/
cryptography - Used for Diffie-Hellman Key Generation and RC4 Encryption

You can install cryptography with:
    $ pip install cryptography


3. How to use

There are three Python files:
    setup.py
    Alice/Host.py
    Bob/Client.py

3.1. setup.py

* Please run this setup.py first before you going to run Host.py and Client.py

It will asks you about the password you going to set.
Generated Diffie-Hellman parameters and hashed password will be stored at Alice/secret.txt

3.2. Alice/Host.py

This is the host-side simulation program.
You must run setup.py before running this program.

After running the Host.py, it will wait for Bob's connection.

After receiving Bob's connection, it will start key exchange with Bob.

You can type exit to exit the connection.

3.3. Bob/Client.py

This is the client-side simulation program.

After running the Client.py, it will wait for your password input.

After you enter the password, it will try connect to Alice and start key exchange with Alice.

You can type exit to exit the connection.
