from django.shortcuts import render
from rest_framework import generics, permissions, response
from .services import *
from .models import *
from .serializers import *
from .permissions import *


class MessageListAPIView(generics.ListAPIView):
    queryset = get_all_messages()
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsChatMember)

    def get_queryset(self):
        last_read: str = self.request.GET.get('last_read')
        last_read_id = 0
        if last_read and last_read.isdigit():
            last_read_id = int(last_read)

        return self.filter_queryset(get_unread_messages(self.kwargs.get('chat_pk'), last_read_id + 1))

    @staticmethod
    def extend_messages(messages, senders):
        data = []
        for message, sender in zip(messages, senders):
            sender: ChatMember

            if sender.user:
                sender_data = {
                    'id': sender.user.pk,
                    'type': 'user',
                    'name': sender.user.username,
                    'first_name': sender.user.first_name,
                    'last_name': sender.user.last_name,

                }
            else:
                sender_data = {
                    'id': sender.bot.pk,
                    'type': 'bot',
                    'name': sender.bot.username,
                    'first_name': sender.bot.first_name,
                    'last_name': sender.bot.last_name,

                }

            data.append({
                'event': 'send',
                'message': message,
                'sender': sender_data
            })
        return data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(
                self.extend_messages(serializer.data, [message.sender for message in queryset]))

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(self.extend_messages(serializer.data, [message.sender for message in queryset]))
