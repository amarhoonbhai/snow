import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from db import get_user_data, update_user_session
from utils import get_user_sessions
from scheduler import start_scheduler, stop_scheduler
from add_group import router as add_group_router
from set_ad import router as set_ad_router
from set_interval import router as set_interval_router
from broadcast import router as broadcast_router

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(add_group_router)
dp.include_router(set_ad_router)
dp.include_router(set_interval_router)
dp.include_router(broadcast_router)

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
    "👋 Welcome to Spinify Ads Main Bot!\n\n"
    "Use /accounts to view your connected accounts.\n"
    "Use /add_group, /set_ad, /set_interval to configure.\n"
    "Use /start_ads to begin automated sending.\n"
    "Use /stop_ads to pause it."
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

@dp.message(Command("start_ads"))
async def start_ads_handler(message: Message):
    start_scheduler()
    await message.answer("✅ Ad automation started.")

@dp.message(Command("stop_ads"))
async def stop_ads_handler(message: Message):
    stop_scheduler()
    await message.answer("🛑 Ad automation stopped.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
