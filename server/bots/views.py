import binascii
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from rest_framework import viewsets, status, response, permissions, generics

from .models import *
from .serializers import *
from .services import *
from .permissions import *


def generate_key(length: int) -> bytes:
    return binascii.hexlify(os.urandom(length // 2))


class BotListCreateAPIView(generics.ListCreateAPIView):
    queryset = get_all_bots()
    serializer_class = CommonBotSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=request.user, token=generate_key(settings.BOT_TOKEN_LENGTH))

        return response.Response(serializer.data)


class BotRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_all_bots()
    serializer_class = ForOwnerBotSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def retrieve(self, request, *args, **kwargs):
        instance: Bot = self.get_object()
        if instance.creator == request.user:
            serializer = ForOwnerBotSerializer(instance)
            return response.Response(serializer.data)
        else:
            serializer = CommonBotSerializer(instance)
            return response.Response(serializer.data)
