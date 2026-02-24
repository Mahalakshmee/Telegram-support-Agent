from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from config import SPREADSHEET_ID,GOOGLE_SA_JSON

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
Spreadsheet_id=SPREADSHEET_ID
RANGE="Sheet1!A2:G"

def get_sheet_data():
    creds = Credentials.from_service_account_file(
        GOOGLE_SA_JSON,  
        scopes=SCOPES
    )

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    response = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE
    ).execute()

    return response.get("values", [])

