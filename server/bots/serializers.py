from rest_framework import serializers
from django.db import models
from .models import *


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ('id', 'creator', 'name')
        extra_kwargs = {
            'creator': {'read_only': True}
        }
