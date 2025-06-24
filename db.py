import sqlite3

conn = sqlite3.connect("delete_times.db", check_same_thread=False)
cur = conn.cursor()

# Create the table to store delete times and message types per group
# We need to handle potential schema migration if the table already exists without the message_type column.
try:
    # Attempt to add the new column if it doesn't exist.
    # This is a common way to handle schema changes in SQLite.
    cur.execute("ALTER TABLE delete_times ADD COLUMN message_type TEXT DEFAULT 'all'")
    conn.commit()
    print("Database schema updated: Added 'message_type' column to 'delete_times' table.")
except sqlite3.OperationalError as e:
    # This typically means the column already exists, which is fine.
    if "duplicate column name" in str(e).lower():
        print("Column 'message_type' already exists in 'delete_times' table.")
    else:
        # Re-raise other operational errors
        raise

cur.execute("""
CREATE TABLE IF NOT EXISTS delete_times (
    chat_id INTEGER PRIMARY KEY,
    delay INTEGER NOT NULL,
    message_type TEXT NOT NULL DEFAULT 'all'
)
""")
conn.commit()

def set_delete_time(chat_id: int, delay: int, message_type: str):
    """Sets or updates the delete time and message type for a given chat_id."""
    cur.execute(
        "REPLACE INTO delete_times (chat_id, delay, message_type) VALUES (?, ?, ?)",
        (chat_id, delay, message_type.lower()) # Ensure message_type is stored in lowercase
    )
    conn.commit()

def get_delete_time(chat_id: int) -> tuple[int, str] | None:
    """Retrieves the delete delay and message type for a given chat_id."""
    cur.execute("SELECT delay, message_type FROM delete_times WHERE chat_id = ?", (chat_id,))
    row = cur.fetchone()
    return (row[0], row[1]) if row else None

def load_all_delete_times() -> dict[int, tuple[int, str]]:
    """Loads all chat_ids with their respective delete delays and message types."""
    cur.execute("SELECT chat_id, delay, message_type FROM delete_times")
    return {chat_id: (delay, message_type) for chat_id, delay, message_type in cur.fetchall()}

def remove_delete_time(chat_id: int):
    """Removes the delete time setting for a given chat_id."""
    cur.execute("DELETE FROM delete_times WHERE chat_id = ?", (chat_id,))
    conn.commit()

# Example usage (optional, for testing):
if __name__ == '__main__':
    # Test functions
    print("Testing DB operations...")
    test_chat_id = 12345

    # Set initial time
    set_delete_time(test_chat_id, 30, "text")
    print(f"Set: {get_delete_time(test_chat_id)}")

    # Update time and type
    set_delete_time(test_chat_id, 60, "media")
    print(f"Updated: {get_delete_time(test_chat_id)}")

    # Set another chat
    set_delete_time(67890, 120, "all")
    print(f"Other chat: {get_delete_time(67890)}")

    # Load all
    all_settings = load_all_delete_times()
    print(f"All settings: {all_settings}")

    # Remove a setting
    remove_delete_time(test_chat_id)
    print(f"After removing {test_chat_id}: {get_delete_time(test_chat_id)}")

    all_settings_after_delete = load_all_delete_times()
    print(f"All settings after delete: {all_settings_after_delete}")

    # Clean up test db (if running this script directly)
    # import os
    # os.remove("delete_times.db")
    # print("Test database cleaned up.")
