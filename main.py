import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from db import get_user_accounts

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "👋 Welcome to SpinAds Bot!\n\n"
        "Use /accounts to view your accounts.\n"
        "Use /add_group, /set_ad, /set_interval to configure."
    )

@dp.message(F.text == "/accounts")
async def accounts_handler(message: Message):
    user_id = message.from_user.id
    accounts = get_user_accounts(user_id)

    if not accounts:
        await message.answer("❌ No accounts found. Please log in via the Login Bot first.")
        return

    text = "🧾 Your connected accounts:\n\n"
    for i, acc in enumerate(accounts, 1):
        username = acc.get("username") or "N/A"
        text += f"{i}. <b>{acc['account_name']}</b> (@{username})\n"

    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
