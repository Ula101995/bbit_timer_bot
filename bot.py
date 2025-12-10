import telebot
from telebot import types

from config import TOKEN, OWNER_ID, GROUP_IDS
from scheduler import close_chat, open_chat

bot = telebot.TeleBot(TOKEN)


# --- Команда /start ---
@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id != OWNER_ID:
        return bot.reply_to(message, "⛔ Sizda ruxsat yo'q.")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔒 Chatni yopish")
    btn2 = types.KeyboardButton("🔓 Chatni ochish")
    markup.add(btn1, btn2)

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
            close_chat(bot, chat_id)
        bot.send_message(message.chat.id, "🔒 Guruhlar yopildi.")

    elif message.text == "🔓 Chatni ochish":
        for chat_id in GROUP_IDS:
            open_chat(bot, chat_id)
        bot.send_message(message.chat.id, "🔓 Guruhlar ochildi.")


# --- Реакция на изменения членов чата ---
@bot.chat_member_handler()
def watch_members(update):
    chat_id = update.chat.id
    new_member = update.new_chat_member

    # Если добавили НАШЕГО бота
    if new_member.user.id == bot.get_me().id:
        bot.send_message(chat_id, "📢 Raqamlashtirish guruhi rasmiy boti ishga tushdi.")
        return

    # Удаление чужих ботов
    if new_member.is_bot and new_member.user.id != bot.get_me().id:
        try:
            bot.ban_chat_member(chat_id, new_member.user.id)
            bot.send_message(chat_id, "❌ Guruhga qo'shilgan begona bot o'chirildi.")
        except:
            pass


print("🤖 Bot ishga tushdi...")

bot.infinity_polling()