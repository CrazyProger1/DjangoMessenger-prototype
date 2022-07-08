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
    print('-------------------------------------------')
    print(message.sender.name + f': {message.id}: ' + message.text)
    user.send_message(message.chat_id, message.text + ' echo')
    print('send output:', message.text + ' echo')


def main():
    user.run_polling(False)


if __name__ == "__main__":
    main()
