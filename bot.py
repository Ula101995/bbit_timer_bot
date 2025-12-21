import telebot
from telebot import types
from telebot.types import ChatPermissions

from config import TOKEN, OWNER_ID, GROUP_IDS

bot = telebot.TeleBot(TOKEN)

# Храним замьюченных пользователей
muted_users = set()


def mute_all(chat_id):
    members = bot.get_chat_administrators(chat_id)
    admins = {admin.user.id for admin in members}

    # Получаем последних пользователей из чата (ограничение API)
    for message in bot.get_chat_history(chat_id, limit=200):
        user = message.from_user
        if not user:
            continue
        if user.id in admins:
            continue
        try:
            bot.restrict_chat_member(
                chat_id,
                user.id,
                ChatPermissions(can_send_messages=False)
            )
            muted_users.add((chat_id, user.id))
        except:
            pass


def unmute_all(chat_id):
    for cid, uid in list(muted_users):
        if cid == chat_id:
            try:
                bot.restrict_chat_member(
                    cid,
                    uid,
                    ChatPermissions(can_send_messages=True)
                )
            except:
                pass
            muted_users.discard((cid, uid))


@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id != OWNER_ID:
        return

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔒 Chatni yopish", "🔓 Chatni ochish")

    bot.send_message(
        message.chat.id,
        "Boshqaruv paneli:",
        reply_markup=kb
    )


@bot.message_handler(func=lambda m: m.from_user.id == OWNER_ID)
def handle_buttons(message):
    if message.text == "🔒 Chatni yopish":
        for gid in GROUP_IDS:
            mute_all(gid)
        bot.send_message(message.chat.id, "🔒 Guruhlar yopildi (mute).")

    elif message.text == "🔓 Chatni ochish":
        for gid in GROUP_IDS:
            unmute_all(gid)
        bot.send_message(message.chat.id, "🔓 Guruhlar ochildi.")


print("🤖 Bot ishga tushdi (mute mode)...")
bot.infinity_polling()
