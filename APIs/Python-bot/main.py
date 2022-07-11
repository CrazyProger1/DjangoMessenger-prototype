import api
from api.message import Message

bot = api.Bot('c3d94ba61f36685b4c50469772e60dff94d63c99b2539152d9')


@bot.message_handler(ignore_my=True)
def handle_message(message: Message):
    print(message.text)
    bot.send_message(message.chat_id, message.text + ' echo')


if __name__ == "__main__":
    bot.authorize()
    bot.run_polling(load_unread_messages=False)
