# Substitution Cipher Program

## Description
This program implements a substitution cipher using a keyword. It supports encryption and decryption of text files.

## Usage
python substitution_cipher.py <keyword> <mode> <input_file> <output_file>

- <keyword>: The keyword to generate the substitution key.
- <mode>: "encrypt" or "decrypt".
- <input_file>: Path to the input file.
- <output_file>: Path to the output file.

## Example
1. Encrypt a file:
   python substitution_cipher.py STRAWBERRY encrypt input.txt encrypted.txt

2. Decrypt a file:
   python substitution_cipher.py STRAWBERRY decrypt encrypted.txt decrypted.txt
