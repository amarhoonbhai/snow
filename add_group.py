from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db import get_user_data, save_user_data

router = Router()

@router.message(Command("add_group"))
async def add_group_handler(message: Message):
    user_id = message.from_user.id
    args = message.text.strip().split()

    if len(args) < 3:
        await message.reply("Usage: /add_group <session_number> <group_id>")
        return

    try:
        session_index = int(args[1]) - 1
        group_id = int(args[2])
    except ValueError:
        await message.reply("Invalid input. Use numeric session number and group ID.")
        return

    user_data = get_user_data(user_id)

    if session_index >= len(user_data["accounts"]):
        await message.reply("Invalid session number. Use /accounts to see your sessions.")
        return

    session_name = user_data["accounts"][session_index]

    # Initialize group list if not exists
    if session_name not in user_data["groups"]:
        user_data["groups"][session_name] = []

    group_list = user_data["groups"][session_name]

    if group_id in group_list:
        await message.reply("This group is already added for the selected account.")
        return

    if len(group_list) < 3:
        group_list.append(group_id)
        await message.reply(f"✅ Group {group_id} added.")
    else:
        replaced = group_list.pop(0)
        group_list.append(group_id)
        await message.reply(f"♻️ Group limit reached. Replaced group {replaced} with {group_id}.")

    save_user_data(user_id, user_data)
