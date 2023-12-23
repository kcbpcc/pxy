import gdown

def upload_file(file_id, local_file_path):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.upload(url, local_file_path, quiet=False)

if __name__ == '__main__':
    DRIVE_FOLDER_ID = '1iEBvg-uH1bRUTAmR2GjiEc_D7fAaxL5R'  # Replace with your folder ID
    LOCAL_FILE_PATH = 'bordpxy.txt'  # Replace with your local file path

    upload_file(DRIVE_FOLDER_ID, LOCAL_FILE_PATH)
