from django.shortcuts import render
from django.db import models

from rest_framework import permissions, viewsets, response, status, generics

from .services import *
from .serializers import *
from .permissions import *


class MyChatMembersListAPIView(generics.ListAPIView):
    queryset = get_all_chat_members()
    serializer_class = ChatMemberSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_my_chats_queryset(self):
        return find_chat_members(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_my_chats_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return response.Response(serializer.data)


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
    permission_classes = (
        permissions.IsAuthenticated,
        IsChatOwnerOrChatIsPublicOrReadOnly,
        IsChatFitOrReadOnly,
        IsInChatOrAddSelfOnly,

    )

    def get_queryset(self):
        chat_id = self.kwargs['chat_pk']
        members = get_chat_members_by_chat_id(chat_id)
        return members

    def validate_not_existing(self):
        if self.request.data.get('user') is not None:
            return find_chat_members(chat=self.kwargs.get('chat_pk'),
                                     user=self.request.data.get('user')).first() is None
        else:
            return find_chat_members(chat=self.kwargs.get('chat_pk'),
                                     user=self.request.data.get('bot')).first() is None

    def perform_create(self, serializer):
        if not self.validate_not_existing():
            raise serializers.ValidationError({'detail', 'Chat member already exists'})

        chat: Chat = get_chat_by_id(self.kwargs.get('chat_pk'))
        serializer.save(chat=chat)
