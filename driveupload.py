import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

def upload_video(file_path):
    SERVICE_ACCOUNT_FILE = os.environ.get("SERVICE_ACCOUNT_JSON")
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("drive", "v3", credentials=creds)

    file_name = os.path.basename(file_path)
    media = MediaFileUpload(file_path, mimetype="video/mp4")
    file_metadata = {"name": file_name}

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"✅ Uploaded {file_name} to Drive, ID: {uploaded_file.get('id')}")
