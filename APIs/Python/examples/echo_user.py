import api
from api.message import Message

user = api.UserModel(
    username='crazy0',
    password='StrongPassword',
    save_tokens=False,
)


@user.message_handler(ignore_my=True)
def handle_message(message: Message):
    user.send_message(message.chat_id, message.text + ' echo')


if __name__ == "__main__":
    user.login()
    user.run_polling(load_unread_messages=False)
