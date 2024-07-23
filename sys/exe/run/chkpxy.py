import os
import subprocess

# Get the current directory
directory = os.path.dirname(os.path.realpath(__file__))

# Get a list of all Python files in the directory (excluding specific files)
exclude_files = ["pxy.py", "webpxy.py", "chkpxy.py", "login_get_kite.py", "rmtknpxy.py"]
python_files = [f for f in os.listdir(directory) if f.endswith(".py") and f not in exclude_files]

# Variables to track success and failure
success_files = []
initial_failures = {}

# Function to run a Python script and handle initial failures
def run_script(file_path):
    try:
        subprocess.check_call(["python", file_path])
        print(f"{file_path} executed successfully.")
        success_files.append(file_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_path}: {e}")
        initial_failures[file_path] = str(e)
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running {file_path}: {e}")
        initial_failures[file_path] = str(e)
        return False

# Run each Python file and check for errors
for file in python_files:
    file_path = os.path.join(directory, file)
    print(f"Running {file}...")

    run_script(file_path)

# Retry failed scripts at the end
retry_failures = {}
for file, error_message in initial_failures.items():
    file_path = os.path.join(directory, file)
    print(f"Retrying {file}...")
    if run_script(file_path):
        print(f"{file} ran successfully after retrying.")
        success_files.append(file)
        del initial_failures[file]  # Remove from initial_failures if succeeded on retry
    else:
        retry_failures[file] = error_message

# Print summary
print("\nSummary:")
if success_files:
    print(f"\033[92m{len(success_files)} files ran successfully:\033[0m")
    for file in success_files:
        print(f"\033[92m{file}\033[0m")
else:
    print("\033[91mNo files ran successfully.\033[0m")

if initial_failures:
    print(f"\033[91m{len(initial_failures)} files failed initially:\033[0m")
    for file, error_message in initial_failures.items():
        print(f"\033[91m{file}: {error_message}\033[0m")

if retry_failures:
    print(f"\033[91m{len(retry_failures)} files failed after retrying:\033[0m")
    for file, error_message in retry_failures.items():
        print(f"\033[91m{file}: {error_message}\033[0m")

if not success_files and not initial_failures and not retry_failures:
    print("\033[91mNo files were processed.\033[0m")

