from django.shortcuts import render
from rest_framework import generics, permissions
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
