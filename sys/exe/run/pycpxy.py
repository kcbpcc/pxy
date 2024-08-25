import py_compile as pc
import os as o
import subprocess
from cryptography.fernet import Fernet

# Function to obtain encryption key from system command
def get_key_from_system():
    # Run the command and get the output
    cmd = "ip link show | grep 'link/ether' | awk '{print $2, $3 \" \" $4}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    key_string = result.stdout.strip()
    
    # Generate a Fernet key from the key_string (make sure it's 32 bytes long)
    key = Fernet.generate_key()
    fernet = Fernet(key)
    encrypted_key = fernet.encrypt(key_string.encode())
    return encrypted_key, fernet

def obfuscate_filename(filename, fernet):
    """Encrypt the filename using the provided Fernet instance."""
    return fernet.encrypt(filename.encode()).decode()

def deobfuscate_filename(encrypted_filename, fernet):
    """Decrypt the filename using the provided Fernet instance."""
    return fernet.decrypt(encrypted_filename.encode()).decode()

def compile_and_delete_files_in_dir(directory, fernet):
    """Compile .py files, obfuscate filenames, and delete original files."""
    for r, d, f in o.walk(directory):
        for fn in f:
            if fn.endswith(".py") and fn != "compile_and_delete.py":
                file_path = o.path.join(r, fn)
                compiled_file_name = obfuscate_filename(fn + 'c', fernet)
                compiled_file_path = o.path.join(r, compiled_file_name)

                try:
                    # Compile the file and save the .pyc in the same directory
                    pc.compile(file_path, cfile=compiled_file_path)
                    print(f"Compiled {file_path} to {compiled_file_path}")

                    # Delete the original .py file if compilation is successful
                    o.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to compile {file_path}: {e}")

if __name__ == "__main__":
    # Obtain the encryption key and Fernet instance
    encrypted_key, fernet = get_key_from_system()

    # Save encrypted_key to a file for later use (decryption)
    with open('encrypted_key.bin', 'wb') as key_file:
        key_file.write(encrypted_key)

    # Get the current directory
    cwd = o.getcwd()

    # Compile all .py files in the current directory and subdirectories, then delete them
    compile_and_delete_files_in_dir(cwd, fernet)

