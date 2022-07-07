from .models import *

from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'sender', 'type', 'text', 'files_password', 'encryption_type', 'sending_datetime')
        extra_kwargs = {
            'sender': {'read_only': True},
            'sending_datetime': {'read_only': True},
            'chat': {'read_only': True}
        }
