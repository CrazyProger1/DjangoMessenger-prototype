from rest_framework import serializers
from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'creator', 'group', 'name')
        extra_kwargs = {
            'creator': {'read_only': True}
        }
