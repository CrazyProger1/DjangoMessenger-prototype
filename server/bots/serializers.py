from rest_framework import serializers
from django.db import models
from .models import *


class PrivateBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'creator', 'name', 'token')
        extra_kwargs = {
            'creator': {'read_only': True},
            'token': {'read_only': True}
        }


class CommonBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('name', 'id')
