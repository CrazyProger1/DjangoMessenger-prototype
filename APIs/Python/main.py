import api
import websocket
import _thread
import time
import rel

user = api.User('crazy7', 'StrongPassword', 'session.json')
user.authorize()


# user.create_bot('ttest')
# user.create_chat('tetschat12', False, False)

# user.add_chat_member(19, user_id=7)


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(close_status_code, close_msg)


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/2/",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close, header={'Authorization': f'Bearer {user.access_token}'})

    ws.run_forever(dispatcher=rel)
    rel.signal(2, rel.abort)
    rel.dispatch()
