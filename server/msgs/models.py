from django.db import models
from django.contrib.auth.models import User
from bots.models import Bot
from chats.models import *


class Message(models.Model):
    chat = models.ForeignKey(Chat, models.CASCADE, verbose_name='chat')
    sender = models.ForeignKey(ChatMember, models.CASCADE, verbose_name='message sender')
    type = models.CharField(verbose_name='message type', max_length=10)
    text = models.BinaryField(verbose_name='message text')
    files_password = models.BinaryField(verbose_name='files password')
    encryption_type = models.CharField(verbose_name='message encryption', max_length=10, default='RSA')
    sending_datetime = models.DateTimeField(verbose_name='sending date and time')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'Message<chat={self.chat.pk}>'
