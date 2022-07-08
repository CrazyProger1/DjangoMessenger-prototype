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


@user.message_handler(ignore_my=True)
def handle_message(message: Message):
    user.send_message(message.chat_id, message.text + '<<')
    print(message.sender.name + f': {message.id}: ' + message.text)

    # if message.sender_id != user.id:
    #     user.send_message(message.chat_id, message.text)


def main():
    user.run_polling()


if __name__ == "__main__":
    main()
