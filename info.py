from os import environ

API_ID = int(environ.get('API_ID', 0))
API_HASH = environ.get('API_HASH', '')
BOT_TOKEN = environ.get('BOT_TOKEN', '')

# Support multiple admin user IDs
# Ensure ADMINS are integers. Filter out non-integer values if any.
admin_env = environ.get('ADMINS', '0')
try:
    ADMINS = list(map(int, admin_env.split()))
except ValueError:
    # Handle cases where ADMINS might be an empty string or contain non-integer values after splitting
    ADMINS = [int(admin_id) for admin_id in admin_env.split() if admin_id.isdigit()]
    if not ADMINS and admin_env != '0': # If parsing failed and it wasn't the default '0'
        print(f"Warning: Could not parse ADMINS environment variable: '{admin_env}'. No admins configured other than potentially '0'.")
        ADMINS = [0] # Default to 0 if parsing fails and it wasn't '0'
    elif not ADMINS and admin_env == '0':
        ADMINS = [0]


# DEL_TIME is removed as per the plan, settings are now per-chat.
# No default MESSAGE_TYPE needed here, it's handled by the database schema ('all')
# and specified in the /settime command.

if __name__ == '__main__':
    # Test cases for ADMINS parsing
    print(f"Raw ADMINS env: '{environ.get('ADMINS')}'")

    environ['ADMINS'] = "123 456 789"
    admin_env = environ.get('ADMINS', '0')
    try:
        ADMINS_TEST = list(map(int, admin_env.split()))
    except ValueError:
        ADMINS_TEST = [int(admin_id) for admin_id in admin_env.split() if admin_id.isdigit()]
    print(f"Parsed ADMINS (expected: [123, 456, 789]): {ADMINS_TEST}")

    environ['ADMINS'] = "123"
    admin_env = environ.get('ADMINS', '0')
    try:
        ADMINS_TEST = list(map(int, admin_env.split()))
    except ValueError:
        ADMINS_TEST = [int(admin_id) for admin_id in admin_env.split() if admin_id.isdigit()]
    print(f"Parsed ADMINS (expected: [123]): {ADMINS_TEST}")

    environ['ADMINS'] = "" # Empty string
    admin_env = environ.get('ADMINS', '0')
    try:
        ADMINS_TEST = list(map(int, admin_env.split()))
    except ValueError: # This will be triggered for empty string
        ADMINS_TEST = [int(admin_id) for admin_id in admin_env.split() if admin_id.isdigit()] if admin_env else [] # Handle empty string explicitly
    if not ADMINS_TEST and admin_env != '0':
         ADMINS_TEST = [0]
    elif not ADMINS_TEST and admin_env == '0': # Default case if env is not set
        ADMINS_TEST = [0]

    print(f"Parsed ADMINS (env empty, expected [0] or from default '0'): {ADMINS_TEST}")

    del environ['ADMINS'] # Unset
    admin_env = environ.get('ADMINS', '0') # Should pick up default '0'
    try:
        ADMINS_TEST = list(map(int, admin_env.split()))
    except ValueError:
        ADMINS_TEST = [int(admin_id) for admin_id in admin_env.split() if admin_id.isdigit()]
    print(f"Parsed ADMINS (env unset, expected [0]): {ADMINS_TEST}")

    environ['ADMINS'] = "123 abc 456" # Mixed
    admin_env = environ.get('ADMINS', '0')
    try:
        ADMINS_TEST = list(map(int, admin_env.split()))
    except ValueError:
        ADMINS_TEST = [int(admin_id) for admin_id in admin_env.split() if admin_id.strip().isdigit()] # Added strip
    if not ADMINS_TEST and admin_env != '0':
        print(f"Warning: Could not parse ADMINS environment variable: '{admin_env}'. No admins configured other than potentially '0'.")
        ADMINS_TEST = [0]
    print(f"Parsed ADMINS (env '123 abc 456', expected [123, 456]): {ADMINS_TEST}")
