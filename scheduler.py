
def close_chat(bot, chat_id):
    try:
        bot.set_chat_permissions(
            chat_id,
            permissions={
                "can_send_messages": False
            }
        )
    except:
        pass


def open_chat(bot, chat_id):
    try:
        bot.set_chat_permissions(
            chat_id,
            permissions={
                "can_send_messages": True
            }
        )
    except:
        pass