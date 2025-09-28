from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from tinydb import TinyDB
import os

router = Router()

ACCOUNTS_DB_PATH = os.getenv("ACCOUNTS_DB_PATH", "../spinauth/accounts.json")
accounts_db = TinyDB(ACCOUNTS_DB_PATH).table("accounts")

OWNER_ID = os.getenv("OWNER_ID")
try:
    OWNER_ID = int(OWNER_ID)
except:
    OWNER_ID = None

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ You are not authorized to use this command.")
        return

    text = message.text.strip().split(maxsplit=1)
    if len(text) < 2:
        await message.answer("Usage: /broadcast <your message>")
        return

    msg = text[1]
    user_ids = set()
    for acc in accounts_db.all():
        user_id = acc.get("user_id")
        if user_id:
            user_ids.add(user_id)

    count = 0
    for uid in user_ids:
        try:
            await message.bot.send_message(uid, msg)
            count += 1
        except Exception as e:
            print(f"Failed to send to {uid}: {e}")

    await message.answer(f"✅ Broadcast sent to {count} user(s).")
