
import telebot
import schedule
import time

from config import TOKEN, GROUP_IDS
from scheduler import close_chat, open_chat

bot = telebot.TeleBot(TOKEN)

def notify_start():
    for chat_id in GROUP_IDS:
        try:
            bot.send_message(chat_id, "🤖 Bot ishga tushdi! Muloqot 17:30–17:32 gacha yopiladi.")
        except:
            pass

# Расписание
schedule.every().day.at("15:30").do(lambda: close_chat(bot))
schedule.every().day.at("15:32").do(lambda: open_chat(bot))

notify_start()

print("Бот запущен...")

while True:
    schedule.run_pending()
    time.sleep(1)