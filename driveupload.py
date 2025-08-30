import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

from auth_utils import get_drive_service



def upload_video(file_path):
    SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_JSON")
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)
    drive_service = get_drive_service()
    media = MediaFileUpload(file_path, mimetype="video/mp4")
    file_metadata = {"name": file_path}

    uploaded_file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"✅ Uploaded {file_path} to Drive, ID: {uploaded_file.get('id')}")
