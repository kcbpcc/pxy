from pydrive.drive import GoogleDrive

def authenticate_drive():
    drive = GoogleDrive()
    return drive

def upload_file(drive, local_file_path, drive_folder_id):
    file_metadata = {
        'title': local_file_path,
        'parents': [{'id': drive_folder_id}]
    }
    file_drive = drive.CreateFile(file_metadata)
    file_drive.Upload()
    print(f'File ID: {file_drive.get("id")}')

if __name__ == '__main__':
    LOCAL_FILE_PATH = 'bordpxy.txt'
    DRIVE_FOLDER_ID = '1iEBvg-uH1bRUTAmR2GjiEc_D7fAaxL5R'

    drive = authenticate_drive()
    upload_file(drive, LOCAL_FILE_PATH, DRIVE_FOLDER_ID)
