from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, response

from .permissions import *
from .models import *
from .serializers import *
from .services import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_all_users()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def retrieve_me(self, request):
        user = request.user
        return response.Response(self.serializer_class(user).data)

