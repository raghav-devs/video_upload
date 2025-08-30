#!/usr/bin/env python3
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from google.cloud import secretmanager

# -----------------------------
# Read secrets from Secret Manager
# -----------------------------
PROJECT_ID = os.environ.get("GCP_PROJECT")
SECRET_NAME = os.environ.get("SERVICE_ACCOUNT_SECRET_NAME")  # e.g. "service-account-json"
VERSION = os.environ.get("SECRET_VERSION", "latest")

client = secretmanager.SecretManagerServiceClient()
secret_path = f"projects/{PROJECT_ID}/secrets/{SECRET_NAME}/versions/{VERSION}"
response = client.access_secret_version(name=secret_path)
service_account_info = response.payload.data.decode("UTF-8")

# Write temp JSON file for service account
import tempfile, json
with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
    f.write(service_account_info)
    SERVICE_ACCOUNT_FILE = f.name

# Video file path (from env)
VIDEO_FILE = os.environ.get("VIDEO_FILE")
UPLOAD_NAME = os.environ.get("UPLOAD_NAME", "uploaded_video.mp4")

if not VIDEO_FILE or not os.path.exists(VIDEO_FILE):
    raise FileNotFoundError(f"Video file not found: {VIDEO_FILE}")

# Authenticate service account
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("drive", "v3", credentials=creds)

# File metadata
file_metadata = {"name": UPLOAD_NAME}
media = MediaFileUpload(VIDEO_FILE, mimetype="video/mp4", resumable=True)

# Resumable upload
request = service.files().create(body=file_metadata, media_body=media, fields="id")
response = None
while response is None:
    status, response = request.next_chunk()
    if status:
        print(f"Uploading... {int(status.progress() * 100)}%")

print("✅ Upload complete. File ID:", response.get("id"))