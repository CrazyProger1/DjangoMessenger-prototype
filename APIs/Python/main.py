import api
import websocket
import _thread
import time
import rel
import json
import threading

user = api.User('crazy7', 'StrongPassword', save_tokens=False)
# user = api.User('admin', 'admin', save_tokens=False)
user.authorize()

# user.add_chat_member(20, user_id=1)


# user.create_bot('ttest')
# user.create_chat('tetschat12', False, False)

# user.add_chat_member(19, user_id=7)
import os


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    pass
    # print(error)


def on_close(ws, close_status_code, close_msg):
    exit(0)


def send_message(ws: websocket.WebSocketApp,
                 message_type: str,
                 text: str,
                 files_password: str):
    ws.send(json.dumps({
        'type': message_type,
        'text': text,
        'files_password': files_password,
        'encryption_type': None,
        'initial': False
    }))


def on_open(ws: websocket.WebSocketApp):
    send_message(ws, 'text', 'hello world!', 'none')


def main():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/20/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close, header={'Authorization': f'Bearer {user.access_token}'},
                                )

    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()


if __name__ == "__main__":
    main()
