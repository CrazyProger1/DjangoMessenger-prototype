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

    def redefine_get_object(self):
        self.get_object = lambda: self.request.user

    def retrieve_me(self, request, *args, **kwargs):
        self.redefine_get_object()
        return self.retrieve(request, *args, **kwargs)

    def destroy_me(self, request, *args, **kwargs):
        self.redefine_get_object()
        return self.destroy(request, *args, **kwargs)

    def update_me(self, request, *args, **kwargs):
        self.redefine_get_object()
        return self.update(request, *args, **kwargs)

    def update_partially_me(self, request, *args, **kwargs):
        self.redefine_get_object()
        return self.partial_update(request, *args, **kwargs)
