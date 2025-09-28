import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from db import get_user_data, update_user_session
from utils import get_user_sessions

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Welcome to Spinify Ads Main Bot!

"
        "Use /accounts to view your connected accounts."
    )

@dp.message(Command("accounts"))
async def accounts_handler(message: Message):
    user_id = message.from_user.id
    sessions = get_user_sessions(user_id)

    if not sessions:
        await message.answer("❌ No accounts found. Please log in using the login bot first.")
        return

    text = "🧾 Your connected accounts:

"
    for i, acc in enumerate(sessions, 1):
        username = acc.get("username") or "N/A"
        name = acc.get("account_name", "Unknown")
        text += f"{i}. <b>{name}</b> (@{username})
"

    await message.answer(text)

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
