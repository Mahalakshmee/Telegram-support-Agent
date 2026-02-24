import sqlite3
import datetime

DB_NAME='chat_data.db'

def setup_db():
    conn=sqlite3.connect(DB_NAME)
    cursor=conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   timestamp TEXT NOT NULL,
                   role TEXT,
                   message_text TEXT NOT NULL)'''
                   )

    conn.commit()
    conn.close()

def save_message(user_id:int,role:str,message_text:str):
    conn=sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO chat_history (user_id, role,timestamp, message_text) VALUES (?, ?, ?,?)",
        (user_id,role, timestamp, message_text)
    )
    conn.commit()
    conn.close()
setup_db()