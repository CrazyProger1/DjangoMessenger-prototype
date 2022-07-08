import api
import websocket
import _thread
import time
import rel
import json
import threading
from api.message import Message

user = api.User('crazy0', 'StrongPassword', save_tokens=False, email_address='crazy@crazy.com')
user.login()


@user.message_handler()
def handle_message(message: Message):
    print(message.text)
    print(message.chat_id)
    print(message.id)
    print(message.sending_datetime)
    print(message.type)


def main():
    user.run_polling()


if __name__ == "__main__":
    main()
