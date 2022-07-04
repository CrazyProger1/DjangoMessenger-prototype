from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets, status, response, permissions

from .models import *
from .serializers import *
from .services import *
from .permissions import *


class BotViewSet(viewsets.ModelViewSet):
    queryset = get_all_bots()
    serializer_class = BotSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            create_bot(**serializer.validated_data, creator=request.user)

        return response.Response(serializer.data)
