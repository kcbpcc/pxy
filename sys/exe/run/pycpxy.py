import py_compile
import os
import subprocess

# Function to obfuscate and compile all .py files in the given directory and its subdirectories
def obfuscate_and_compile_files_in_dir(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "compile_and_delete.py":
                file_path = os.path.join(root, filename)
                obfuscated_file_path = os.path.join(root, filename + '.obf')

                try:
                    # Obfuscate the file
                    subprocess.run(["pyarmor", "obfuscate", file_path, "-O", root], check=True)
                    print(f"Obfuscated {file_path} to {obfuscated_file_path}")

                    # Compile the obfuscated file
                    compiled_file_path = os.path.join(root, filename + 'c')
                    py_compile.compile(obfuscated_file_path, cfile=compiled_file_path)
                    print(f"Compiled {obfuscated_file_path} to {compiled_file_path}")

                    # Delete the original and obfuscated .py files if compilation is successful
                    os.remove(file_path)
                    os.remove(obfuscated_file_path)
                    print(f"Deleted {file_path} and {obfuscated_file_path}")
                except Exception as e:
                    print(f"Failed to obfuscate or compile {file_path}: {e}")

# Get the current directory
current_dir = os.getcwd()

# Obfuscate and compile all .py files in the current directory and subdirectories, then delete them
obfuscate_and_compile_files_in_dir(current_dir)


