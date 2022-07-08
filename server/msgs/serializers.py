from rest_framework.utils.serializer_helpers import ReturnDict

from .models import *

from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'chat', 'type', 'text', 'files_password', 'encryption_type', 'sending_datetime')
        extra_kwargs = {
            'sending_datetime': {'read_only': True},
            'chat': {'read_only': True}
        }
