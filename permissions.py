import time
from telebot.types import ChatPermissions
from telebot.apihelper import ApiTelegramException

MAX_RETRIES = 3
RETRY_DELAY = 1.5  # seconds


def set_permissions_with_retry(chat_id, permissions):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            bot.set_chat_permissions(chat_id, permissions)
            print(f"✅ Success for chat {chat_id}")
            return True

        except ApiTelegramException as e:
            print(
                f"⚠️ Attempt {attempt}/{MAX_RETRIES} failed for {chat_id}: {e}"
            )

            # No point retrying if the bot has no rights
            if "not enough rights" in str(e).lower():
                print(f"🚫 Permanent failure for {chat_id}, skipping retries.")
                return False

            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

        except Exception as e:
            print(f"🔥 Unexpected error for {chat_id}: {e}")
            return False

    print(f"❌ All retries failed for chat {chat_id}")
    return False
