import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import MessageMediaType
from db import get_delete_time, load_all_delete_times

# Dictionary to keep track of scheduled deletion tasks
# chat_id -> {message_id: asyncio.Task}
scheduled_tasks = {}

async def delete_message_after_delay(message: Message, delay: int):
    """Coroutine to delete a message after a specified delay."""
    await asyncio.sleep(delay)
    try:
        await message.delete()
        # Clean up the task from the dictionary
        chat_id = message.chat.id
        if chat_id in scheduled_tasks and message.message_id in scheduled_tasks[chat_id]:
            del scheduled_tasks[chat_id][message.message_id]
            if not scheduled_tasks[chat_id]: # Remove chat_id if no tasks left
                del scheduled_tasks[chat_id]
    except Exception as e:
        print(f"Error deleting message {message.message_id} in chat {message.chat.id}: {e}")

@Client.on_message(filters.group & ~filters.service, group=1) # group=1 to process after commands
async def auto_delete_handler(client: Client, message: Message):
    chat_id = message.chat.id
    settings = get_delete_time(chat_id)

    if not settings:
        return

    delay, message_type_to_delete = settings

    if delay <= 0: # Should not happen if /settime validates correctly
        return

    # Determine the type of the current message
    current_message_type = "text" # Default for text messages or messages with no specific media type
    if message.media:
        if message.media in [
            MessageMediaType.PHOTO,
            MessageMediaType.VIDEO,
            MessageMediaType.ANIMATION,
            MessageMediaType.AUDIO,
            MessageMediaType.DOCUMENT,
            MessageMediaType.STICKER,
            MessageMediaType.VOICE,
            MessageMediaType.VIDEO_NOTE,
        ]:
            current_message_type = "media"
        # Add other specific media types if needed, or group them.
        # For example, if message.sticker or message.photo etc.

    # Check if this message should be deleted based on type
    should_delete = False
    if message_type_to_delete == "all":
        should_delete = True
    elif message_type_to_delete == "text":
        # A message is considered 'text' for deletion if it has text content AND no media.
        # The 'current_message_type' variable already helps distinguish this.
        # If message.media was present, current_message_type would be 'media'.
        # So, if current_message_type is 'text', it implies no media.
        # We also need to ensure there's actual text for it to be a "text message".
        if current_message_type == "text" and message.text:
            should_delete = True
    elif message_type_to_delete == "media" and current_message_type == "media":
        should_delete = True

    if should_delete:
        # Schedule the deletion
        task = asyncio.create_task(delete_message_after_delay(message, delay))
        if chat_id not in scheduled_tasks:
            scheduled_tasks[chat_id] = {}
        scheduled_tasks[chat_id][message.message_id] = task
        # print(f"Scheduled message {message.message_id} in chat {chat_id} for deletion in {delay}s.")

async def load_initial_tasks(client: Client):
    """
    This function would ideally re-schedule deletions for messages that were sent
    while the bot was offline and whose deletion time hasn't passed yet.
    However, this is complex because we'd need to fetch recent message history for each
    configured chat and check their timestamps.
    For simplicity, this initial version will not re-schedule old messages.
    It will primarily ensure that the bot loads settings and is ready for new messages.
    """
    print("Loading auto-delete settings for all chats...")
    all_settings = load_all_delete_times()
    # In a more advanced version, one might iterate through client.get_chat_history()
    # for chats in all_settings to find messages that should have been deleted
    # but weren't due to downtime. This is non-trivial due to rate limits and message IDs.
    print(f"Loaded settings for {len(all_settings)} chats.")


# It's good practice to call load_initial_tasks when the bot starts.
# This can be done in the main bot.py or via a Client event handler.
# For now, we'll rely on the bot loading settings as messages come in.
# A more robust solution would use a startup hook if Pyrogram supports it easily,
# or call it from main bot script after client.start().

# Example of how you might hook it into client startup (conceptual)
# This would typically be done in your main bot file or a plugin that loads early.
# @Client.on_event("startup") # This is a placeholder for actual event handling
# async def startup_event_handler(client: Client):
# await load_initial_tasks(client)
# print("Auto-delete plugin loaded and initial tasks (if any) are being processed.")
