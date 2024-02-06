'''
import env
from utils import *

driveScopes = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.appdata",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata",
    "https://www.googleapis.com/auth/drive.scripts",
]

googleScopes = driveScopes

from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

import os
import webbrowser
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"


def write_creds(file, creds):
    year = datetime.now().year
    nextYear = year + 1
    a = '"' + str(year)
    b = '"' + str(nextYear)
    data = creds.to_json().replace(a, b)
    write(file, data)
    return creds

def servicer( key="drive", reset=False):
    versions = {
        "classroom": {"version": "v1"},
        "drive": {"version": "v3", "method": "files"},
        "sheets": {"version": "v4", "method": "spreadsheets"},
        "spreadsheets": {"version": "v4", "method": "spreadsheets"},
        "gmail": {"version": "v1"},
        "docs": {"version": "v1"},
        "youtube": {"version": "v3"},
        "search": {"version": "v1", "name": "customsearch"},
    }

    ref = versions.get(key)
    version = ref.get("version")
    token_file = "/home/kdog3682/2024/token.json"

    creds = setup_credentials(token_file, reset)
    service = build(key, version, credentials=creds)
    print("returning successful service", key)
    if ref.get("method"):
        return getattr(service, ref.get("method"))()
    return service


def setup_credentials(token_file, reset = False):
    def get_credentials():
        flow = (
            InstalledAppFlow.from_client_secrets_file(
                token_file, googleScopes
            )
        )
        return flow.run_local_server(port=0)

    if reset:
        return write_creds(token_file, get_credentials())
    if is_file(token_file):
        try:
            return Credentials.from_authorized_user_file(
                token_file, googleScopes
            )
        except Exception as e:
            prompt(str(e))
            return write_creds(token_file, get_credentials())
    # if creds.expired:
        # return write_creds(token_file, creds.refresh(Request()))

# print(get_service("gmail"))
# print(get_service("classroom"))

google_drive_fields = [
    'id',
    'name',
    'mimeType',
    'description',
    'starred',
    'trashed',
    'explicitlyTrashed',
    'parents',
    'properties',
    'appProperties',
    'spaces',
    'version',
    'webContentLink',
    'webViewLink',
    'iconLink',
    'thumbnailLink',
    'viewedByMe',
    'viewedByMeTime',
    'createdTime',
    'modifiedTime',
    'modifiedByMeTime',
    'sharedWithMeTime',
    'sharingUser',
    'owners',
    'lastModifyingUser',
    'shared',
    'folderColorRgb',
    'originalFilename',
    'fullFileExtension',
    'fileExtension',
    'md5Checksum',
    'size',
    'quotaBytesUsed',
    'headRevisionId',
    'contentHints',
    'imageMediaMetadata',
    'videoMediaMetadata',
    'isAppAuthorized'
]

mime_types = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
    "svg": "image/svg+xml",
    "pdf": "application/pdf",
    "txt": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json",
    "xml": "application/xml",
    "zip": "application/zip",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "mp4": "video/mp4",
    "mov": "video/quicktime",
    "avi": "video/x-msvideo",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
    "document": "application/vnd.google-apps.document",
    "spreadsheet": "application/vnd.google-apps.spreadsheet",
    "doc": "application/vnd.apps.document",
    "sheet": "application/vnd.google-apps.spreadsheet",
    "slide": "application/vnd.google-apps.presentation",
    "folder": "application/vnd.google-apps.folder"
}


def open(self):
    url = self
    if hasattr(self, "url"):
        url = self.url
    webbrowser.open(url)

def resolve_mime_type(x):
    return mime_types.get(x)

def resolve_id(x):
    if is_string(x):
        if is_google_id(x):
            return x
        else:
            panic("not a valid google id", x)
    elif is_object(x):
        if 'documentId' in x: return x.get('documentId')
        elif 'id' in x: return x.get('id')
        elif 'spreadsheetId' in x: return x.get('spreadsheetId')

    panic("x must be a string or an object", x)

service = servicer(key = "drive", reset = True)
print(service)
'''


from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

file = '/mnt/chromeos/MyFiles/Downloads/rapid-math-367217-db54781cd484.json'
creds = Credentials.from_authorized_user_file(file)

# Build the service object
service = build('drive', 'v3', credentials=creds)
print(service)
