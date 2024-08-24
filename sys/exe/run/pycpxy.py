import py_compile
import os

# Function to compile all .py files in the given directory and its subdirectories
def compile_and_delete_files_in_dir(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "compile_and_delete.py":
                # Define the full path of the .py and .pyc files
                file_path = os.path.join(root, filename)
                compiled_file_path = os.path.join(root, filename + 'c')
                
                try:
                    # Compile the file and save the .pyc in the same directory
                    py_compile.compile(file_path, cfile=compiled_file_path)
                    print(f"Compiled {file_path} to {compiled_file_path}")
                    
                    # Delete the original .py file if compilation is successful
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to compile {file_path}: {e}")

# Get the current directory
current_dir = os.getcwd()

# Compile all .py files in the current directory and subdirectories, then delete them
compile_and_delete_files_in_dir(current_dir)
