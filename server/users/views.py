from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, response, permissions, decorators, status

from .permissions import *
from .models import *
from .serializers import *
from .services import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)

    def get_object(self):
        if self.kwargs.get('pk') is not None:
            return super(UserViewSet, self).get_object()
        return self.request.user
