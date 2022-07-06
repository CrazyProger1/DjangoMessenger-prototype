from django.shortcuts import render
from django.db import models

from rest_framework import permissions, viewsets, response, status, generics

from .services import *
from .serializers import *
from .permissions import *


class ChatViewSet(viewsets.ModelViewSet):
    queryset = get_all_chats()
    serializer_class = ChatSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        chat = serializer.save(creator=self.request.user)
        ChatMember(user=self.request.user, chat=chat).save()


class ChatMemberViewSet(viewsets.ModelViewSet):
    queryset = get_all_chat_members()
    serializer_class = ChatMemberSerializer
    permission_classes = (permissions.IsAuthenticated, IsChatOwnerOrChatIsPublicOrReadOnly)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        members = get_chat_members_by_chat_id(chat_id)
        return members

    def perform_create(self, serializer):
        chat: Chat = get_chat_by_id(self.kwargs.get('pk'))
        serializer.save(chat=chat)
