import shutil
import os

def remove_contents(directory):
    try:
        # Construct the full path
        full_path = os.path.join(os.path.expanduser("~"), directory)
        
        # Check if the directory exists
        if os.path.exists(full_path):
            # Remove all contents of the directory
            shutil.rmtree(full_path)
            print("Let's clean up 📇 and prepare to switch ♻️")
        else:
            print("Let's clean up 📇 and prepare to switch ♻️")
    except Exception as e:
        print(f"Error occurred: {e}")

# Specify the directory whose contents you want to remove
directory_path = "pxy/sys/exe/data"
remove_contents(directory_path)
