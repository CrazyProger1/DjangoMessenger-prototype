import api
import websocket
import _thread
import time
import rel
import json
import threading

user = api.User('crazy0', 'StrongPassword', save_tokens=False, email_address='crazy@crazy.com')
user.login()


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    pass


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


def connect_to_chat(chat_id: int):
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(f"ws://127.0.0.1:8000/ws/chat/{chat_id}/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header={'Authorization': f'Bearer {user.access_token}'})

    ws.run_forever(dispatcher=rel)


def main():
    connect_to_chat(1)
    connect_to_chat(2)

    rel.signal(2, rel.abort)
    rel.dispatch()


if __name__ == "__main__":
    main()
