from rest_framework import serializers
from django.db import models
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'first_name', 'last_name')
