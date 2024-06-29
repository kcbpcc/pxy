import os

def remove_contents(directory):
    try:
        # Construct the full path
        full_path = os.path.join(os.path.expanduser("~"), directory)
        
        # Check if the directory exists
        if os.path.exists(full_path):
            # Iterate over all the files and directories in the specified directory
            for filename in os.listdir(full_path):
                file_path = os.path.join(full_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove file or symbolic link
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove directory and all its contents
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            print("Let's clean up 📇 and prepare to switch ♻️")
        else:
            print(f"The directory {full_path} does not exist.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Specify the directory whose contents you want to remove
directory_path = "pxy/sys/exe/data"
remove_contents(directory_path)
