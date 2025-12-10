import telebot
from telebot import types
from config import TOKEN, OWNER_ID, GROUP_IDS

bot = telebot.TeleBot(TOKEN)

# --- Функции управления чатом ---

def close_chat(chat_id):
    """Закрыть чат — запретить всем писать."""
    perms = telebot.types.ChatPermissions(can_send_messages=False)
    bot.set_chat_permissions(chat_id, perms)
    bot.send_message(chat_id, "🔒 *Muloqot yopildi!*", parse_mode="Markdown")

def open_chat(chat_id):
    """Открыть чат — разрешить писать."""
    perms = telebot.types.ChatPermissions(can_send_messages=True)
    bot.set_chat_permissions(chat_id, perms)
    bot.send_message(chat_id, "🔓 *Muloqot ochildi!*", parse_mode="Markdown")

# --- Команда /start ---

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "⛔ Sizda ruxsat yo'q.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔒 Chatni yopish", "🔓 Chatni ochish")

    bot.send_message(
        message.chat.id,
        "🤖 Boshqaruv paneli:",
        reply_markup=markup
    )

# --- Обработка кнопок ---

@bot.message_handler(func=lambda msg: msg.from_user.id == OWNER_ID)
def handle_buttons(message):
    if message.text == "🔒 Chatni yopish":
        for chat_id in GROUP_IDS:
            close_chat(chat_id)
        bot.send_message(message.chat.id, "🔒 Guruhlar yopildi.")

    elif message.text == "🔓 Chatni ochish":
        for chat_id in GROUP_IDS:
            open_chat(chat_id)
        bot.send_message(message.chat.id, "🔓 Guruhlar ochildi.")

# --- Реакция на события участников чата ---

@bot.chat_member_handler()
def watch_members(update):
    chat_id = update.chat.id
    new_member = update.new_chat_member

    # Если добавили твоего бота
    if new_member.user.id == bot.get_me().id:
        bot.send_message(chat_id, "📢 Raqamlashtirish guruhi rasmiy boti ishga tushdi.")
        return

    # Если добавили чужого бота
    if new_member.is_bot and new_member.user.id != bot.get_me().id:
        try:
            bot.ban_chat_member(chat_id, new_member.user.id)
            bot.send_message(chat_id, "❌ Guruhga qo'shilgan begona bot o'chirildi.")
        except:
            pass

print("🤖 Bot ishga tushdi...")
bot.infinity_polling()