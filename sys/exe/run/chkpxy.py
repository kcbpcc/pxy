import os
import subprocess

# Get the current directory
directory = os.path.dirname(os.path.realpath(__file__))

# Get a list of all Python files in the directory (excluding specific files)
exclude_files = ["pxy.pyc", "webpxy.pyc", "chkpxy.pyc", "login_get_kite.pyc", "rmtknpxy.pyc"]
python_files = [f for f in os.listdir(directory) if f.endswith(".pyc") and f not in exclude_files]

# Variables to track success and failure
success_files = []
initial_failures = {}
retry_success_files = []
retry_failures = {}

# Function to run a Python script and handle initial failures
def run_script(file_path):
    try:
        subprocess.check_call(["python", file_path])
        print(f"{file_path} executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {file_path}: {e}")
        return str(e)
    except Exception as e:
        print(f"An unexpected error occurred while running {file_path}: {e}")
        return str(e)

# Run each Python file and check for errors
for file in python_files:
    file_path = os.path.join(directory, file)
    print(f"Running {file}...")

    result = run_script(file_path)
    if result is True:
        success_files.append(file)
    else:
        initial_failures[file] = result

# Retry failed scripts at the end
for file, error_message in list(initial_failures.items()):
    file_path = os.path.join(directory, file)
    print(f"Retrying {file}...")
    result = run_script(file_path)
    if result is True:
        retry_success_files.append(file)
        del initial_failures[file]  # Remove from initial_failures if succeeded on retry
    else:
        retry_failures[file] = error_message

# Calculate summary details
total_tests = len(python_files)
initial_successes = len(success_files)
retry_successes = len(retry_success_files)
total_failures = len(initial_failures) + len(retry_failures)

# Print detailed summary
if success_files:
    print(f"\033[92mSuccess on first attempt ({len(success_files)}):\033[0m")
    for file in success_files:
        print(f"  - \033[92m{file}\033[0m")
else:
    print("\033[91mNo files ran successfully on first attempt.\033[0m")

if retry_success_files:
    print(f"\033[92mSuccess on second attempt ({len(retry_success_files)}):\033[0m")
    for file in retry_success_files:
        print(f"  - \033[92m{file}\033[0m")
else:
    print("\033[91mNo files ran on second attempt.\033[0m")

if initial_failures:
    print(f"\033[91mFailures after first attempt ({len(initial_failures)}):\033[0m")
    for file, error_message in initial_failures.items():
        print(f"  - \033[91m{file}\033[0m: {error_message}")

if retry_failures:
    print(f"\033[91mFailures after second attempt ({len(retry_failures)}):\033[0m")
    for file, error_message in retry_failures.items():
        print(f"  - \033[91m{file}\033[0m: {error_message}")

if not success_files and not retry_success_files and not initial_failures and not retry_failures:
    print("\033[91mNo files were processed.\033[0m")
else:
    print("\nProcessing complete.")

# Print overall summary
print("\nSummary:")
print("=" * 40)
print(f"Total files tested: {total_tests}")
print(f"\033[92mSuccessful on first attempt: {initial_successes}\033[0m")
print(f"\033[92mSuccessful on second attempt: {retry_successes}\033[0m")
print(f"\033[91mTotal failures: {total_failures}\033[0m")
print("=" * 40)
