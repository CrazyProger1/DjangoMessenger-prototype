import api
import websocket
import _thread
import time
import rel
import json
import threading
from api.message import Message

user = api.User('admin', 'admin', save_tokens=False, email_address='crazy@crazy.com')
user.login()


def main():
    user.send_message(2, input('>>'))


if __name__ == "__main__":
    main()
