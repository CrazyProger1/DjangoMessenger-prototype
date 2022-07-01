from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .permissions import *
from .models import *
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)
