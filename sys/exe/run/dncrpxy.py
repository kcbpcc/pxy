import sys
import os
import base64
from cryptography.fernet import Fernet

# Fixed key (must match the encryption key)
fixed_key = b"089608"

# Expand the key to 32 bytes by padding
key = fixed_key.ljust(32, b'\0')[:32]  # Ensure the key is exactly 32 bytes
fernet_key = base64.urlsafe_b64encode(key)  # Convert to base64
cipher_suite = Fernet(fernet_key)

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
    try:
        decrypted_code = cipher_suite.decrypt(encrypted_code)
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

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

