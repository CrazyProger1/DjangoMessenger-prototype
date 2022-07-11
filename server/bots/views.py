import binascii
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from rest_framework import viewsets, status, response, permissions, generics, mixins

from .models import *
from .serializers import *
from .services import *
from .permissions import *


def generate_key(length: int) -> str:
    return binascii.hexlify(os.urandom(length // 2)).decode('utf-8')


class BotListCreateAPIView(generics.ListCreateAPIView):
    queryset = get_all_bots()
    serializer_class = CommonBotSerializer
    permission_classes = (IsAuthenticatedOrBot,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, token=generate_key(settings.BOT_TOKEN_LENGTH))

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class() if self.request.method != 'POST' else PrivateBotSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class BotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_bots()
    serializer_class = PrivateBotSerializer
    permission_classes = (IsAuthenticatedOrBot, IsOwnerOrReadOnly)

    def retrieve(self, request, *args, **kwargs):
        bot = kwargs.get('bot')
        instance: Bot = self.get_object()
        if instance.creator == request.user or (bot and bot.pk == kwargs.get('pk')):
            serializer = PrivateBotSerializer(instance)
            return response.Response(serializer.data)
        else:
            serializer = CommonBotSerializer(instance)
            return response.Response(serializer.data)


class BotRetrieveAPIView(
    generics.RetrieveAPIView
):
    queryset = get_all_bots()
    serializer_class = PrivateBotSerializer
    permission_classes = (IsBot,)

    def get_object(self):
        obj = self.kwargs.get('bot')
        if obj:
            return obj
        return super(BotRetrieveAPIView, self).get_object()

