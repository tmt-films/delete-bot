import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from db import set_delete_time, get_delete_time
from info import ADMINS

# Helper function to parse time string (e.g., "10s", "5m", "1h")
def parse_time(time_str: str) -> int:
    time_str = time_str.lower()
    if time_str.endswith("s"):
        return int(time_str[:-1])
    elif time_str.endswith("m"):
        return int(time_str[:-1]) * 60
    elif time_str.endswith("h"):
        return int(time_str[:-1]) * 3600
    else:
        raise ValueError("Invalid time format. Use s, m, or h.")

@Client.on_message(filters.command("settime") & filters.group & filters.user(ADMINS))
async def settime_command(client: Client, message: Message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("Usage: /settime <delay> [type]\nExample: /settime 10s all\nTypes: all, text, media")
        return

    delay_str = message.command[1]
    message_type = "all"  # Default to all
    if len(message.command) > 2:
        msg_type_arg = message.command[2].lower()
        if msg_type_arg in ["all", "text", "media"]:
            message_type = msg_type_arg
        else:
            await message.reply_text("Invalid message type. Use 'all', 'text', or 'media'.")
            return

    try:
        delay_seconds = parse_time(delay_str)
        if delay_seconds <= 0:
            await message.reply_text("Delete time must be a positive value.")
            return
        set_delete_time(chat_id, delay_seconds, message_type)
        await message.reply_text(f"Auto-delete time for this chat set to {delay_str} for '{message_type}' messages.")
    except ValueError as e:
        await message.reply_text(f"Error: {e}")
    except Exception as e:
        await message.reply_text(f"An unexpected error occurred: {e}")

@Client.on_message(filters.command("deltime") & filters.group & filters.user(ADMINS))
async def deltime_command(client: Client, message: Message):
    chat_id = message.chat.id
    settings = get_delete_time(chat_id)
    if settings:
        delay, message_type = settings
        # Convert delay back to a human-readable format (optional, but good for UX)
        if delay % 3600 == 0:
            delay_str = f"{delay // 3600}h"
        elif delay % 60 == 0:
            delay_str = f"{delay // 60}m"
        else:
            delay_str = f"{delay}s"
        await message.reply_text(f"Current auto-delete setting for this chat: {delay_str} for '{message_type}' messages.")
    else:
        await message.reply_text("Auto-delete is not currently configured for this chat. Use /settime to configure it.")

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    await message.reply_text("Hello! I'm an auto-delete bot. Add me to a group and make me an admin to get started.\n"
                             "Use /settime <delay> [type] in the group to configure auto-deletion (e.g., /settime 30s all).\n"
                             "Only group admins can use the commands.")

# Basic ping command to check if the bot is alive
@Client.on_message(filters.command("ping"))
async def ping_command(client: Client, message: Message):
    await message.reply_text("Pong!")
