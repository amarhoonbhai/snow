from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("set_interval"))
async def set_interval_handler(message: types.Message):
    args = message.text.split()

    if len(args) != 3:
        await message.reply("Usage:\n/set_interval <session_number> <interval_minutes>")
        return

    try:
        session_number = int(args[1])
        interval_minutes = int(args[2])
    except ValueError:
        await message.reply("❌ Both session and interval must be numbers.")
        return

    # TODO: Save interval setting to DB
    await message.reply(f"✅ Interval set for session {session_number}: every {interval_minutes} minutes.")
