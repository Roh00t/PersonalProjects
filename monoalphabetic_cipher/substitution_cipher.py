import string
import argparse
import os

def generate_key(keyword):
    """
    Generate the substitution key based on the keyword.
    """
    # Remove duplicates from the keyword while maintaining order
    unique_keyword = "".join(dict.fromkeys(keyword.upper()))
    
    # Append the rest of the alphabet in reverse order
    remaining_alphabet = [ch for ch in reversed(string.ascii_uppercase) if ch not in unique_keyword]
    substitution_key = unique_keyword + "".join(remaining_alphabet)
    
    return substitution_key

def encrypt(message, key):
    """
    Encrypt the message using the substitution key.
    """
    alphabet = string.ascii_uppercase
    encryption_table = str.maketrans(alphabet, key)
    return message.upper().translate(encryption_table)

def decrypt(ciphertext, key):
    """
    Decrypt the ciphertext using the substitution key.
    """
    alphabet = string.ascii_uppercase
    decryption_table = str.maketrans(key, alphabet)
    return ciphertext.upper().translate(decryption_table)

def read_file(file_path):
    """
    Read content from a file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """
    Write content to a file.
    """
    with open(file_path, 'w') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description="Substitution Cipher with File I/O")
    parser.add_argument("keyword", help="Keyword to generate the substitution cipher key")
    parser.add_argument("mode", choices=["encrypt", "decrypt"], help="Mode: encrypt or decrypt")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    
    args = parser.parse_args()

    try:
        # Generate the substitution key
        key = generate_key(args.keyword)
        print(f"Substitution Key: {key}")

        # Read input from file
        input_text = read_file(args.input_file)
        print(f"Input text read from {args.input_file}")

        # Perform encryption or decryption
        if args.mode == "encrypt":
            output_text = encrypt(input_text, key)
        elif args.mode == "decrypt":
            output_text = decrypt(input_text, key)

        # Write output to file
        write_file(args.output_file, output_text)
        print(f"Output written to {args.output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
