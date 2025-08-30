import os
import tempfile
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_drive_service():
    """
    Reads service account JSON from env var (mounted from Secret Manager),
    writes to a temp file, and returns a Drive API client.
    """
    service_account_info = os.getenv("SERVICE_ACCOUNT_JSON")
    if not service_account_info:
        raise ValueError("SERVICE_ACCOUNT_JSON env var not set.")

    # Write secret to a temp file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(service_account_info)
        service_account_file = f.name

    # Build creds from temp file
    creds = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    # Return Drive service client
    return build("drive", "v3", credentials=creds)


def get_gcs_client():
    """
    Reads service account JSON from env var, writes to a temp file,
    and returns a Cloud Storage client.
    """
    from google.cloud import storage

    service_account_info = os.getenv("SERVICE_ACCOUNT_JSON")
    if not service_account_info:
        raise ValueError("SERVICE_ACCOUNT_JSON env var not set.")

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(service_account_info)
        service_account_file = f.name

    return storage.Client.from_service_account_json(service_account_file)
