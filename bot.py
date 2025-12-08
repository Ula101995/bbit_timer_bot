
import telebot
import schedule
import time

from config import TOKEN, GROUP_IDS
from scheduler import close_chat, open_chat

bot = telebot.TeleBot(TOKEN)

def notify_start():
    for chat_id in GROUP_IDS:
        try:
            bot.send_message(chat_id, "🤖 Raqamlashtirish guruhi rasmiy Boti ishga tushdi! Muloqot 18:30 dan 08:00 gacha yopiladi.")
        except:
            pass

# Расписание
schedule.every().day.at("13:30").do(lambda: close_chat(bot))
schedule.every().day.at("03:00").do(lambda: open_chat(bot))

notify_start()

print("Bot ishga tushdi...")

while True:
    schedule.run_pending()
    time.sleep(1)