# FILE STRUCTURE
Encryption_Toolkit/
├── scripts/
│   ├── encryptor.py       # Core implementation of encryption algorithms
│   ├── test_encryptor.py  # Script to test encryption and decryption
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation

# Project Overview
## Objective:
Implement and demonstrate encryption and decryption using 3DES, Twofish, RC4, and AES.
Compare their performance and security features

## Installations:
Step 1: Install Dependencies
pip install -r requirements.txt

Step 2: Run the Test Script
python scripts/test_encryptor.py

## Key Features
AES: Advanced Encryption Standard for secure symmetric encryption.
3DES: Triple Data Encryption Standard for legacy applications.
RC4: Stream cipher for quick encryption (though deprecated).
Twofish: A block cipher alternative to AES.
ECC: Secure public-key cryptography for signing and key exchange.
PGP: Strong encryption and signing using the RSA algorithm.

# Conclusion
This complete toolkit helps you understand and experiment with these cryptographic algorithms.