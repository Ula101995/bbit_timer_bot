import telebot
from telebot import types
from telebot.types import ChatPermissions

from config import TOKEN, OWNER_ID, GROUP_IDS

bot = telebot.TeleBot(TOKEN)
print("=== Проверка групп ===")
for gid in GROUP_IDS:
    try:
        chat = bot.get_chat(gid)
        print(f"OK: {gid} | type={chat.type} | title={chat.title}")
    except Exception as e:
        print(f"FAIL: {gid} -> {e}")
print("=== Конец проверки ===")
#bot.infinity_polling()

# Храним состояние чатов (закрыт/открыт)
chat_closed = {gid: False for gid in GROUP_IDS}


def mute_user(chat_id, user_id):
    try:
        bot.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(can_send_messages=False)
        )
    except:
        pass


def unmute_user(chat_id, user_id):
    try:
        bot.restrict_chat_member(
            chat_id,
            user_id,
            ChatPermissions(can_send_messages=True)
        )
    except:
        pass


def mute_all(chat_id):
    admins = {a.user.id for a in bot.get_chat_administrators(chat_id)}
    # Мьютим тех, кто писал недавно (ограничение Telegram API)
    try:
        for msg in bot.get_chat_history(chat_id, limit=200):
            if msg.from_user and msg.from_user.id not in admins:
                mute_user(chat_id, msg.from_user.id)
    except:
        pass
    chat_closed[chat_id] = True


def unmute_all(chat_id):
    admins = {a.user.id for a in bot.get_chat_administrators(chat_id)}
    try:
        for msg in bot.get_chat_history(chat_id, limit=200):
            if msg.from_user and msg.from_user.id not in admins:
                unmute_user(chat_id, msg.from_user.id)
    except:
        pass
    chat_closed[chat_id] = False


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
            mute_all(gid)
        bot.send_message(message.chat.id, "🔒 Barcha guruhlar yopildi (mute).")

    elif message.text == "🔓 Chatni ochish":
        for gid in GROUP_IDS:
            unmute_all(gid)
        bot.send_message(message.chat.id, "🔓 Barcha guruhlar ochildi.")


@bot.chat_member_handler()
def on_new_member(update):
    chat_id = update.chat.id
    user = update.new_chat_member.user

    # Уведомление при добавлении бота
    if user.id == bot.get_me().id:
        bot.send_message(chat_id, "📢 Raqamlashtirish guruhi rasmiy boti ishga tushdi.")
        return

    # Если чат закрыт — мутим новых
    if chat_closed.get(chat_id):
        mute_user(chat_id, user.id)


print("🤖 Bot ishga tushdi (MUTE MODE)...")
bot.infinity_polling()
