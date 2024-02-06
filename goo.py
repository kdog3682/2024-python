import os.path
from foo import googleScopes
from hoo import

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "/mnt/chromeos/MyFiles/Downloads/rapid-math-367217-db54781cd484.json"

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=googleScopes)


service = build("drive", "v3", credentials=credentials)
print(service)

