import json

from channels.generic import websocket
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User, AnonymousUser


class ChatConsumer(websocket.WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        websocket.WebsocketConsumer.__init__(self, *args, **kwargs)

        self.user: User | AnonymousUser | None = None
        self.chat_id = 0
        self.chat_group_name = ''

    def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.chat_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json.get('message')
        print(message)

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event.get('message')

        self.send(
            text_data=json.dumps({
                'event': 'send',
                'message': message
            })
        )
