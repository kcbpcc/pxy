import sys
import os
import socket
import hashlib
from cryptography.fernet import Fernet

# Step 1: Get the hostname and generate the key
hostname = socket.gethostname()
key = hashlib.sha256(hostname.encode()).digest()
cipher_suite = Fernet(Fernet.generate_key())

# Step 2: Decrypt the content of the file and execute it
def decrypt_and_execute(filename):
    with open(filename, 'rb') as encrypted_file:
        encrypted_code = encrypted_file.read()

    # Decrypt the code
    decrypted_code = cipher_suite.decrypt(encrypted_code)

    # Execute the decrypted code
    exec(decrypted_code, globals())

# Step 3: Use this script by passing the encrypted filename as an argument
if len(sys.argv) != 2:
    print("Usage: python decrypt_and_run.py <filename.py>")
    sys.exit(1)

filename = sys.argv[1]

if os.path.exists(filename) and filename.endswith('.py'):
    decrypt_and_execute(filename)
else:
    print(f"File {filename} does not exist or is not a Python file.")
