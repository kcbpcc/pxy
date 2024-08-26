import sys
import os
import socket
import hashlib
from cryptography.fernet import Fernet

# Generate the same key as used during encryption
hostname = socket.gethostname()
key = hashlib.sha256(hostname.encode()).digest()
cipher_suite = Fernet(Fernet.generate_key())

ENCRYPTION_MARKER = b"# ENCRYPTED FILE\n"

def decrypt_and_execute(filename):
    with open(filename, 'rb') as encrypted_file:
        encrypted_code = encrypted_file.read()

    # Check if the file is marked as encrypted
    if not encrypted_code.startswith(ENCRYPTION_MARKER):
        print(f"Error: {filename} does not appear to be encrypted or is corrupted.")
        return

    # Remove the marker and decrypt the code
    encrypted_code = encrypted_code[len(ENCRYPTION_MARKER):]
    decrypted_code = cipher_suite.decrypt(encrypted_code)

    # Execute the decrypted code
    exec(decrypted_code, globals())

if len(sys.argv) != 2:
    print("Usage: python decrypt_and_run.py <filename.py>")
    sys.exit(1)

filename = sys.argv[1]

if os.path.exists(filename) and filename.endswith('.py'):
    decrypt_and_execute(filename)
else:
    print(f"File {filename} does not exist or is not a Python file.")

