import telebot
from telebot import types
from telebot.types import ChatPermissions

from config import TOKEN, OWNER_ID, GROUP_IDS

bot = telebot.TeleBot(TOKEN)


def close_chat(chat_id):
    bot.set_chat_permissions(
        chat_id,
        ChatPermissions(
            can_send_messages=False,
            can_send_media_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False
        )
    )


def open_chat(chat_id):
    bot.set_chat_permissions(
        chat_id,
        ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
            can_change_info=False,
            can_invite_users=True,
            can_pin_messages=False
        )
    )


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id != OWNER_ID:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔒 Chatni yopish", "🔓 Chatni ochish")

    bot.send_message(message.chat.id, "Boshqaruv paneli:", reply_markup=kb)


@bot.message_handler(func=lambda m: m.from_user.id == OWNER_ID)
def handle_buttons(message):
    if message.text == "🔒 Chatni yopish":
        for gid in GROUP_IDS:
            close_chat(gid)
        bot.send_message(message.chat.id, "🔒 Barcha guruhlar yopildi.")

    elif message.text == "🔓 Chatni ochish":
        for gid in GROUP_IDS:
            open_chat(gid)
        bot.send_message(message.chat.id, "🔓 Barcha guruhlar ochildi.")


@bot.chat_member_handler()
def on_bot_added(update):
    if update.new_chat_member.user.id == bot.get_me().id:
        bot.send_message(
            update.chat.id,
            "📢 Raqamlashtirish guruhi rasmiy boti ishga tushdi."
        )


print("🤖 Bot ishga tushdi...")
bot.infinity_polling()
