from dotenv import load_dotenv
import os
load_dotenv()

TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
GOOGLE_CREDENTIAL_PATH = os.getenv("cred.json")
SPREADSHEET_ID=os.getenv("SPREADSHEET_ID")
GOOGLE_SA_JSON=os.getenv("GOOGLE_SA_JSON")
SYNC_CRON=os.getenv("SYNC_CRON","hourly")
GOOGLE_APPLICATION_CREDENTIALS=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
CLIENT_ID=os.getenv("CLIENT_ID")
CLIENT_SECRET=os.getenv("SECRET")
REFRESH_TOKEN=os.getenv("REFRESH_TOKEN")
EMAIL_USER=os.getenv("SENDER_EMAIL")