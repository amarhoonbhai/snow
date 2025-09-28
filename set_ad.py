from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db import get_user_data, save_user_data

router = Router()

@router.message(Command("set_ad"))
async def set_ad_handler(message: Message):
    user_id = message.from_user.id
    args = message.text.strip().split(maxsplit=2)

    if len(args) < 3:
        await message.reply("Usage: /set_ad <session_number> <ad_message>")
        return

    try:
        session_index = int(args[1]) - 1
    except ValueError:
        await message.reply("Invalid session number.")
        return

    ad_message = args[2]
    user_data = get_user_data(user_id)

    if session_index >= len(user_data["accounts"]):
        await message.reply("Invalid session number. Use /accounts to view your sessions.")
        return

    session_name = user_data["accounts"][session_index]
    user_data["ads"][session_name] = ad_message

    save_user_data(user_id, user_data)
    await message.reply("✅ Ad message saved for this account.")
