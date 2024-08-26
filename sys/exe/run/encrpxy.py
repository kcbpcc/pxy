import os
import base64
from cryptography.fernet import Fernet

# Fixed key (shorter than needed, so we will pad it)
fixed_key = b"089608"

# Expand the key to 32 bytes by padding (e.g., with zeros)
key = fixed_key.ljust(32, b'\0')[:32]  # Ensure the key is exactly 32 bytes
fernet_key = base64.urlsafe_b64encode(key)  # Convert to base64
cipher_suite = Fernet(fernet_key)

# Define the encryption marker
ENCRYPTION_MARKER = b"# ENCRYPTED FILE\n"

# Encrypt and overwrite all .py files in the directory
for filename in os.listdir():
    if filename.endswith('.py') and filename != 'encrypt_files.py':  # Exclude this encryption script itself
        with open(filename, 'rb') as file:
            original_code = file.read()

        # Check if the file is already encrypted
        if original_code.startswith(ENCRYPTION_MARKER):
            print(f"Skipping {filename}: Already encrypted.")
            continue

        # Prepend the marker and encrypt the file
        encrypted_code = ENCRYPTION_MARKER + cipher_suite.encrypt(original_code)

        # Overwrite the original file with the encrypted content
        with open(filename, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_code)

print("Encryption complete.")
