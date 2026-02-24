from __future__ import print_function
from datetime import datetime, timedelta
import pytz
import dateparser
from langchain_core.chat_history import InMemoryChatMessageHistory
import pickle
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_core.tools import Tool
from langchain.agents import create_agent,AgentState
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional,TypedDict,List
from langchain_community.chat_message_histories import ChatMessageHistory
from typing import Dict,Any
from langchain_core.prompts import ChatPromptTemplate
from system_prompt import llm,system_prompt_text
import subprocess, json
from subprocess import CalledProcessError


SCOPES = ["https://www.googleapis.com/auth/calendar"]

store: Dict[str, ChatMessageHistory] = {}

meeting_keywords = [
        "schedule", "meeting", "book", "arrange",
        "appointment", "call", "set up", "fix",
        "talk", "consultation"
    ]
class CustomState(AgentState,total=False):
    input: str       
    chat_history: List[Any]
    deal_confirmed: bool
    meeting_locked: bool
class MeetingArgs(BaseModel):
    summary: Optional [str] = Field(default="General Meeting", description="Meeting title")
    start_dt: str = Field(..., description="The natural language string for the start date and time (e.g., 'tomorrow at 1:30 PM')")
    end_dt: str = Field(..., description="The natural language string for the end date and time or duration (e.g., 'for one hour' or 'tomorrow at 2:30 PM')")
    session_id: Optional [str] = None

class EmailArgs(BaseModel):
    product_name: str = Field(..., description="Name of the purchased product")
    final_price: float = Field(..., description="Final price of the product")


def get_calendar_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('calendar_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(summary, start_dt, end_dt,attendees=None):
    service = get_calendar_service()
    tz = pytz.timezone("Asia/Kolkata")
    if start_dt.tzinfo is None:
        start_dt = tz.localize(start_dt)
    if end_dt.tzinfo is None:
        end_dt = tz.localize(end_dt)


    event = {
        'summary': summary,
        'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'attendees': [{'email': email} for email in attendees] if attendees else [],
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def parse_natural_datetime(text):
    tz = pytz.timezone("Asia/Kolkata")
    now = tz.localize(datetime(2025, 12, 1, 19, 29))  # current time in IST
    dt = dateparser.parse(
        text,
        settings={
            "TIMEZONE": "Asia/Kolkata",
            "TO_TIMEZONE": "Asia/Kolkata",
            "RETURN_AS_TIMEZONE_AWARE": True,
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": now   # ✅ important for "tomorrow", "next week"
        }
    )
    return dt



def execute_workflow(summary: str, start_dt: str, end_dt: str, session_id: Optional[str] = None):
    

    # 3. Localize the naive datetime objects to the correct timezone (IST)
    start_dt_aware = parse_natural_datetime(start_dt)
    end_dt_aware = parse_natural_datetime(end_dt)
    
    # 4. Call create_event with the localized (timezone-aware) objects
    event_link = create_event(summary, start_dt_aware, end_dt_aware)

    return f"""
✅ Meeting Scheduled Successfully!
📝 Title: {summary}
📅 Date: {start_dt_aware.date()}
⏰ Time: {start_dt_aware.time()}
🔗 Event Link: {event_link}
"""

def send_email(product_name: str, final_price: float):
    import subprocess, json
    subprocess.run([
        "node",
        "gmail.js",
        json.dumps({
            "productName": product_name,
            "finalPrice": final_price
        })
    ])
    return "✅ Email sent successfully."
    
schedule_meeting_tool =StructuredTool.from_function(
    name="schedule_meeting",
    description="Schedules a meeting after extracting meeting details from user message.",
    func=execute_workflow,
    args_schema=MeetingArgs,
    return_direct=True
    
)

send_email_tool =StructuredTool.from_function(
    name="email_sending",
    description="Sending Email after the deal closes",
    func=send_email,
    args_schema=EmailArgs,
    return_direct=True
    
)

agent = create_agent(
    model=llm,
    tools=[schedule_meeting_tool,send_email_tool],
    system_prompt=system_prompt_text,
    state_schema=CustomState,
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a scheduling assistant"),
    ("human", "{input}")
])

session_histories = {}

def get_user_memory(user_id: int):
    if user_id not in session_histories:
        session_histories[user_id] = InMemoryChatMessageHistory()
    return session_histories[user_id]

