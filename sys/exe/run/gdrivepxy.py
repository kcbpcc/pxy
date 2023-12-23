from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and handles authentication.

    drive = GoogleDrive(gauth)
    return drive

def upload_file(drive, local_file_path, drive_folder_id):
    file_metadata = {
        'title': os.path.basename(local_file_path),
        'parents': [{'id': drive_folder_id}]
    }
    file_drive = drive.CreateFile(file_metadata)
    file_drive.Upload()
    print(f'File ID: {file_drive.get("id")}')

if __name__ == '__main__':
    LOCAL_FILE_PATH = 'bordpxy.txt'  # Use a relative path if the file is in the same directory
    DRIVE_FOLDER_ID = '1iEBvg-uH1bRUTAmR2GjiEc_D7fAaxL5R'  # Use the folder ID from the shared link

    drive = authenticate_drive()
    upload_file(drive, LOCAL_FILE_PATH, DRIVE_FOLDER_ID)
