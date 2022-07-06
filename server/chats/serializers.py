from rest_framework import serializers
from .models import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'creator', 'group', 'name', 'private')
        extra_kwargs = {
            'creator': {'read_only': True}
        }


class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = ('id', 'user', 'bot', 'chat')
