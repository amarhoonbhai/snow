from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db import get_user_data, save_user_data

router = Router()

VALID_INTERVALS = [20, 40, 60]

@router.message(Command("set_interval"))
async def set_interval_handler(message: Message):
    user_id = message.from_user.id
    args = message.text.strip().split()

    if len(args) != 3:
        await message.reply("Usage: /set_interval <session_number> <interval_minutes>
Valid intervals: 20, 40, 60")
        return

    try:
        session_index = int(args[1]) - 1
        interval = int(args[2])
    except ValueError:
        await message.reply("Invalid input. Use numbers only.")
        return

    if interval not in VALID_INTERVALS:
        await message.reply("❌ Invalid interval. Choose from: 20, 40, 60 minutes.")
        return

    user_data = get_user_data(user_id)

    if session_index >= len(user_data["accounts"]):
        await message.reply("Invalid session number. Use /accounts to view your sessions.")
        return

    session_name = user_data["accounts"][session_index]
    user_data["intervals"][session_name] = interval

    save_user_data(user_id, user_data)
    await message.reply(f"✅ Interval set to {interval} minutes for session #{session_index + 1}.")
