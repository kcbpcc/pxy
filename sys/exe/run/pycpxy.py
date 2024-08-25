import os
from setuptools import setup
from Cython.Build import cythonize

# Function to compile and obfuscate .py files in the given directory and its subdirectories
def compile_and_delete_files_in_dir(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py") and filename != "compile_and_delete.py":
                file_path = os.path.join(root, filename)
                
                # Convert .py file to .pyx file
                pyx_file_path = os.path.join(root, filename.replace(".py", ".pyx"))
                with open(file_path, 'r') as py_file:
                    with open(pyx_file_path, 'w') as pyx_file:
                        pyx_file.write(py_file.read())
                
                # Create setup.py content for Cython compilation
                setup_content = f"""
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("{filename.replace(".py", ".pyx")}")
)
"""
                
                setup_file_path = os.path.join(root, 'setup.py')
                with open(setup_file_path, 'w') as setup_file:
                    setup_file.write(setup_content)
                
                try:
                    # Compile the .pyx file to a C extension
                    os.system(f"python {setup_file_path} build_ext --inplace")
                    compiled_file_path = os.path.join(root, filename.replace(".py", ".pyd"))
                    
                    # Check if compilation was successful
                    if os.path.exists(compiled_file_path):
                        print(f"Compiled {file_path} to {compiled_file_path}")
                        
                        # Delete the original .py and .pyx files
                        os.remove(file_path)
                        os.remove(pyx_file_path)
                        os.remove(setup_file_path)
                        print(f"Deleted {file_path} and {pyx_file_path}")
                    else:
                        print(f"Failed to compile {file_path}")
                except Exception as e:
                    print(f"Failed to compile {file_path}: {e}")

# Get the current directory
current_dir = os.getcwd()

# Compile all .py files in the current directory and subdirectories, then delete them
compile_and_delete_files_in_dir(current_dir)


