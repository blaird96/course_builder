# services/google/common.py
from __future__ import annotations
from pathlib import Path
from typing import Optional, Tuple, List
from datetime import timedelta, date

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive.file"]
SCOPES_CAL   = ["https://www.googleapis.com/auth/calendar.events"]

# Paths (project root)
CREDENTIALS_PATH = Path("credentials.json")
TOKEN_PATH       = Path("token.json")

def get_credentials(scopes: List[str]) -> Optional[Credentials]:
    """
    Returns valid Credentials. Uses token.json cache if present; otherwise runs OAuth flow.
    Returns None if credentials are not available or invalid.
    """
    creds: Optional[Credentials] = None
    
    try:
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_PATH.exists() or CREDENTIALS_PATH.stat().st_size == 0:
                    print(f"[WARNING] credentials.json is missing or empty. Google services will be skipped.")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), scopes)
                creds = flow.run_local_server(port=0)
            TOKEN_PATH.write_text(creds.to_json())

        return creds
    except Exception as e:
        print(f"[WARNING] Failed to get Google credentials: {e}")
        print("[WARNING] Google services will be skipped.")
        return None

def build_drive():
    creds = get_credentials(SCOPES_DRIVE)
    if creds is None:
        return None
    return build("drive", "v3", credentials=creds)

def build_calendar():
    creds = get_credentials(SCOPES_CAL)
    if creds is None:
        return None
    return build("calendar", "v3", credentials=creds)

def ensure_drive_folder(service, name: str, parent_id: Optional[str] = None) -> str:
    """
    Find or create a Google Drive folder by name (optionally under parent). Returns folder ID.
    Note: name-based lookup is idempotent-ish but not unique if duplicates exist.
    """
    q = "mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    safe_name = name.replace("'", r"\'")
    q += f" and name = '{safe_name}'"
    
    if parent_id:
        q += f" and '{parent_id}' in parents"

    resp = service.files().list(q=q, fields="files(id,name)", pageSize=1).execute()
    files = resp.get("files", [])
    if files:
        return files[0]["id"]

    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        meta["parents"] = [parent_id]
    folder = service.files().create(body=meta, fields="id").execute()
    return folder["id"]

def all_day_exclusive_range(start_inclusive: date, end_inclusive: date) -> Tuple[str, str]:
    """
    Google Calendar all-day events require an exclusive end date.
    Returns (start_date, end_exclusive_date) ISO strings.
    """
    return (start_inclusive.isoformat(), (end_inclusive + timedelta(days=1)).isoformat())
