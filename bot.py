import telebot
from telebot import types

from config import TOKEN, GROUP_IDS
from scheduler import close_chat, open_chat

bot = telebot.TeleBot(TOKEN)

# 🔐 Только твой ID — остальные админом быть не могут
ADMIN_ID = 67763298


# ----------------------------------------------------------
# 🔥 Автоматическое удаление чужих ботов + уведомление
# ----------------------------------------------------------
@bot.chat_member_handler()
def check_new_member(update):
    new_user = update.new_chat_member.user

    # Если это бот И он не наш собственный бот → удалить
    if new_user.is_bot and new_user.id != bot.get_me().id:
        try:
            for gid in GROUP_IDS:
                bot.ban_chat_member(gid, new_user.id)
                bot.send_message(gid, "❌ Guruhga qo‘shilgan begona bot o‘chirildi.")
            print(f"❌ Uchinchi bot o‘chirildi: {new_user.id}")
        except Exception as e:
            print("Xato:", e)


# ----------------------------------------------------------
# 🔧 ADMIN PANEL (только для тебя)
# ----------------------------------------------------------
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "⛔ Sizda ruxsat yo’q!")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🔒 Chatni yopish")
    btn2 = types.KeyboardButton("🔓 Chatni ochish")
    keyboard.add(btn1, btn2)

    bot.send_message(message.chat.id, "🔧 Admin panel:", reply_markup=keyboard)


@bot.message_handler(func=lambda m: True)
def admin_actions(message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text == "🔒 Chatni yopish":
        close_chat(bot)
        bot.send_message(message.chat.id, "🔒 Chat yopildi!")

    elif message.text == "🔓 Chatni ochish":
        open_chat(bot)
        bot.send_message(message.chat.id, "🔓 Chat ochildi!")


print("Бот запущен...")

bot.polling(none_stop=True)