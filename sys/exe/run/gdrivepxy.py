from gupload import GoogleDriveUpload

def upload_file(file_id, local_file_path):
    GoogleDriveUpload().upload(local_file_path, file_id)

if __name__ == '__main__':
    DRIVE_FOLDER_ID = '1iEBvg-uH1bRUTAmR2GjiEc_D7fAaxL5R'  # Replace with your folder ID
    LOCAL_FILE_PATH = 'bordpxy.txt'  # Replace with your local file path

    upload_file(DRIVE_FOLDER_ID, LOCAL_FILE_PATH)
