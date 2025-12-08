
import telebot
from telebot import types
from config import GROUP_IDS

def close_chat(bot: telebot.TeleBot):
    for chat_id in GROUP_IDS:
        try:
            bot.send_message(chat_id, "🔒 Muloqot ertalabki 08:00 gacha yopildi.")
            bot.set_chat_permissions(chat_id, types.ChatPermissions(can_send_messages=False))
        except Exception as e:
            print(f"[ERROR close_chat] {e}")

def open_chat(bot: telebot.TeleBot):
    for chat_id in GROUP_IDS:
        try:
            bot.send_message(chat_id, "✅ Muloqot ochildi!")
            bot.set_chat_permissions(chat_id, types.ChatPermissions(can_send_messages=True))
        except Exception as e:
            print(f"[ERROR open_chat] {e}")