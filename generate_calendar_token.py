from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def generate_calendar_token():
    if os.path.exists("token_calendar.pickle"):
        os.remove("token_calendar.pickle")

    flow = InstalledAppFlow.from_client_secrets_file(
        "calendar_credentials.json",
        SCOPES
    )

    creds = flow.run_local_server(port=0)

    with open("token_calendar.pickle", "wb") as token:
        pickle.dump(creds, token)

    print("✅ Calendar token generated: token_calendar.pickle")

generate_calendar_token()
