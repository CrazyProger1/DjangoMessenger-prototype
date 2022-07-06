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
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        members = get_chat_members_by_chat_id(chat_id)
        return members

    def perform_create(self, serializer):
        try:
            serializer.save(chat=get_chat_by_id(self.kwargs.get('pk')))
        except models.ObjectDoesNotExist:
            raise serializers.ValidationError({'chat': 'Chat with this id does not exist.'})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
