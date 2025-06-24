# 🧹 Telegram Auto-Delete Bot (Pyrogram)

This is a simple Telegram bot built using **Pyrogram**. It automatically deletes messages in group chats after a specified delay (like `10s`, `2m`, `1hr`) and message type (all, text, or media). Settings are persisted using **SQLite**, so timers and configurations remain active even after bot restarts.

---

## ⚙️ Features

- Set auto-delete timer and message type per group using `/settime`.
- Specify whether to delete `all` messages, only `text` messages, or only `media` messages.
- Check current timer and message type settings using `/deltime`.
- Auto-delete messages matching the configuration after the specified delay.
- Admin-only access control for configuration commands.
- Persistent settings using SQLite.
- Basic `/start` and `/ping` commands.

---

## 🚀 Commands

| Command                 | Description                                                                 | Access       |
|-------------------------|-----------------------------------------------------------------------------|--------------|
| `/settime <delay> [type]` | Set message delete timer and type.                                          | Admins only  |
|                         | `delay`: e.g., `10s`, `5m`, `1h`.                                           |              |
|                         | `type` (optional, defaults to `all`): `all`, `text`, `media`.               |              |
|                         | Example: `/settime 30m text` (delete text messages after 30 minutes)        |              |
|                         | Example: `/settime 1h media` (delete media messages after 1 hour)           |              |
|                         | Example: `/settime 10s` (delete all messages after 10 seconds)              |              |
| `/deltime`              | Show current auto-delete delay and message type for the chat.               | Admins only  |
| `/start`                | Show a welcome message (primarily for private chat with the bot).           | All users    |
| `/ping`                 | Check if the bot is responsive.                                             | All users    |

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/telegram-auto-delete-bot.git # Replace with the actual repo URL
cd telegram-auto-delete-bot
```

### 2. Configuration
Create a `.env` file in the root directory or set environment variables:
```env
API_ID="YOUR_API_ID"
API_HASH="YOUR_API_HASH"
BOT_TOKEN="YOUR_BOT_TOKEN"
ADMINS="ADMIN_USER_ID_1 ADMIN_USER_ID_2" # Space-separated list of admin User IDs
```
- `API_ID` and `API_HASH`: Get these from [my.telegram.org](https://my.telegram.org/apps).
- `BOT_TOKEN`: Get this from [BotFather](https://t.me/BotFather) on Telegram.
- `ADMINS`: Numerical Telegram User IDs of users who are allowed to use admin commands.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Bot
```bash
python bot.py
```

### 5. Add to Group
- Add your bot to the desired Telegram group.
- Promote the bot to an admin within the group so it has permission to delete messages.
- Use the `/settime` command in the group to configure the auto-deletion rules.

---

## Notes

- **Media Messages**: "Media" includes photos, videos, animations, audio files, documents, stickers, voice messages, and video notes.
- **Text Messages**: "Text" includes messages that are purely text content without any attached media. Messages with captions and media are treated based on their media component if "media" type is chosen for deletion, or as "all" if "all" is chosen. If "text" is chosen, only messages with no media are targeted.

This project is for educational purposes and can be expanded with more features.
Make sure your bot has the necessary permissions in the group (e.g., "Delete messages") to function correctly.
