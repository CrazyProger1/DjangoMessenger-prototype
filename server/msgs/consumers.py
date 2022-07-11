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
from bots.extractors import extract_bot_from_scope


class ChatConsumer(websocket.WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        websocket.WebsocketConsumer.__init__(self, *args, **kwargs)

        self.user: User | AnonymousUser | None = None
        self.bot: Bot | None = None
        self.chat_id = 0
        self.chat_group_name = ''
        self.chat: Chat | None = None
        self.connection_accepted = False
        self.chat_member: ChatMember | None = None

    def connect(self):
        self.user: User = self.scope['user']
        self.bot = extract_bot_from_scope(self.scope)
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        try:
            self.chat = get_chat_by_id(self.chat_id)

            if self.user.is_authenticated:
                self.chat_member = find_chat_members(chat=self.chat_id, user=self.user.pk).first()
            elif self.bot:
                self.chat_member = find_chat_members(chat=self.chat_id, bot=self.bot.pk).first()

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
        json_message = json.loads(text_data)

        serializer = MessageSerializer(data=json_message)
        if not serializer.is_valid():
            print('NOT VALID!')  # add handler
            return

        serializer.save(sending_datetime=timezone.now(), sender=self.chat_member, chat=self.chat)

        if self.user.is_authenticated:
            sender = {
                'id': self.user.pk,
                'type': 'user',
                'name': self.user.username,
                'first_name': self.user.first_name,
                'last_name': self.user.last_name,
            }
        else:
            sender = {
                'id': self.bot.pk,
                'type': 'bot',
                'name': self.bot.name
            }

        async_to_sync(self.channel_layer.group_send)(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': serializer.data,
                'sender': sender
            }
        )

    def chat_message(self, event):
        message_data = event.get('message')
        sender_data = event.get('sender')

        self.send(
            text_data=json.dumps({
                'event': 'send',
                'message': message_data,
                'sender': sender_data
            })
        )
