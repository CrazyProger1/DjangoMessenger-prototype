import json
from channels.generic import websocket
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User, AnonymousUser
from django.utils import timezone

from chats.models import Chat
from chats.services import *
from django.db import models
from channels import exceptions
from .models import *
from .serializers import *
from .services import *


class ChatConsumer(websocket.WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        websocket.WebsocketConsumer.__init__(self, *args, **kwargs)

        self.user: User | AnonymousUser | None = None
        self.chat_id = 0
        self.chat_group_name = ''
        self.chat: Chat | None = None
        self.connection_accepted = False
        self.chat_member: ChatMember | None = None

    def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        try:
            self.chat = get_chat_by_id(self.chat_id)
            self.chat_member = find_chat_members(chat=self.chat_id, user=self.user.pk).first()

            if self.chat_member is None:
                raise models.ObjectDoesNotExist('Chat member matching query does not exists')

            self.chat_group_name = f'chat_{self.chat_id}'

            async_to_sync(self.channel_layer.group_add)(
                self.chat_group_name,
                self.channel_name
            )

            self.accept()

            self.connection_accepted = True

        except models.ObjectDoesNotExist as e:
            raise exceptions.DenyConnection(e)

    def disconnect(self, code):
        if self.connection_accepted:
            async_to_sync(self.channel_layer.group_discard)(
                self.chat_group_name,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        message = json.loads(text_data)
        print(message)
        serializer = MessageSerializer(data=message)
        if not serializer.is_valid():
            print('not valid!')
            return

        serializer.save(sending_datetime=timezone.now(), sender=self.chat_member, chat=self.chat)

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

# active_users = {}
#
#
# class SimpleTestChatConsumer(websocket.WebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         websocket.WebsocketConsumer.__init__(self, *args, **kwargs)
#         print('init')
#
#         self.user: User | AnonymousUser | None = None
#         self.chat_id = 0
#         self.chat_group_name = ''
#         self.chat: Chat | None = None
#         self.connection_accepted = False
#         self.chat_member: ChatMember | None = None
#
#     def connect(self):
#         self.user = self.scope['user']
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#
#         try:
#             self.chat = get_chat_by_id(self.chat_id)
#             self.chat_member = find_chat_members(chat=self.chat.pk, user=self.user.pk).first()
#
#             if self.chat_member is None:
#                 raise models.ObjectDoesNotExist('Chat member matching query does not exists')
#
#             if self.chat_id not in active_users.keys():
#                 active_users.update({self.chat_id: [self.chat_member]})
#             else:
#                 active_users.get(self.chat_id).append(self.chat_member)
#
#             self.chat_group_name = f'chat_{self.chat_id}'
#             self.user_group_name = f'user_{self.user.pk}'
#
#             async_to_sync(self.channel_layer.group_add)(
#                 self.user_group_name,
#                 self.channel_name
#             )
#
#             self.accept()
#
#             self.connection_accepted = True
#
#         except models.ObjectDoesNotExist as e:
#             raise exceptions.DenyConnection(e)
#
#     def disconnect(self, code):
#         if self.connection_accepted:
#             async_to_sync(self.channel_layer.group_discard)(
#                 self.chat_group_name,
#                 self.channel_name
#             )
#
#             active_users.get(self.chat_id).remove(self.chat_member)
#
#     def receive(self, text_data=None, bytes_data=None):
#         print('data:', text_data)
#         # text_data_json = json.loads(text_data)
#         # print(text_data_json)
#         # message = text_data_json.get('message')
#         # print(message)
#         message = self.user.username + ': ' + text_data
#         async_to_sync(self.channel_layer.group_send)(
#             self.user_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message
#             }
#         )
#
#     def chat_message(self, event):
#         message = event.get('message')
#
#         self.send(
#             text_data=json.dumps({
#                 'event': 'send',
#                 'message': message
#             })
#         )
