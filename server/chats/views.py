from django.shortcuts import render

from rest_framework import permissions, viewsets, response, status

from .services import *
from .serializers import *
from .permissions import *


class ChatViewSet(viewsets.ModelViewSet):
    queryset = get_all_chats()
    serializer_class = ChatSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
