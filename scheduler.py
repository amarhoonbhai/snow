import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from tinydb import TinyDB, Query
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from datetime import datetime

# Load config
USER_DB_PATH = os.getenv("USER_DATA_DB", "user_data.json")
ACCOUNTS_DB_PATH = os.getenv("ACCOUNTS_DB_PATH", "../spinauth/accounts.json")
user_db = TinyDB(USER_DB_PATH).table("users")
accounts_db = TinyDB(ACCOUNTS_DB_PATH).table("accounts")

scheduler = AsyncIOScheduler()

def get_session_string(session_name):
    Account = Query()
    acc = accounts_db.get(Account.session_name == session_name)
    return acc.get("session_string") if acc else None

async def send_ads_for_user(user):
    for session_name in user.get("accounts", []):
        groups = user.get("groups", {}).get(session_name, [])
        ad = user.get("ads", {}).get(session_name)
        interval = user.get("intervals", {}).get(session_name)

        if not ad or not groups or not interval:
            continue

        session_str = get_session_string(session_name)
        if not session_str:
            continue

        try:
            client = TelegramClient(StringSession(session_str), 12345, 'dummyhash')  # ID/hash are not used here
            await client.connect()
            for group_id in groups:
                try:
                    await client.send_message(group_id, ad)
                    print(f"[{datetime.now()}] Sent ad to {group_id}")
                except Exception as e:
                    print(f"❌ Error sending to {group_id}: {e}")
            await client.disconnect()
        except Exception as e:
            print(f"❌ Failed session {session_name}: {e}")

def schedule_user_ads():
    for user in user_db.all():
        for session_name in user.get("accounts", []):
            interval = user.get("intervals", {}).get(session_name)
            if interval:
                job_id = f"{user['user_id']}_{session_name}"
                scheduler.add_job(
                    send_ads_for_user,
                    args=[user],
                    trigger='interval',
                    minutes=interval,
                    id=job_id,
                    replace_existing=True
                )

def start_scheduler():
    schedule_user_ads()
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown(wait=False)
