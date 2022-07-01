from django.db import models
from django.contrib.auth.models import User
from bots.models import Bot


class Chat(models.Model):
    creator = models.ForeignKey(User, models.CASCADE, verbose_name='chat creator')
    group = models.BooleanField(verbose_name='group')
    name = models.CharField(verbose_name='chat name', max_length=200)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

    def __str__(self):
        return f'Chat<group={self.group}>'


class ChatMember(models.Model):
    user = models.ForeignKey(User, models.CASCADE, verbose_name='user', null=True)
    bot = models.ForeignKey(Bot, models.CASCADE, verbose_name='bot', null=True)
    chat = models.ForeignKey(Chat, models.CASCADE, verbose_name='chat')

    class Meta:
        verbose_name = 'Chat member'
        verbose_name_plural = 'Chat members'

    @property
    def is_bot(self):
        return self.bot is not None

    def __str__(self):
        return f'Chat member<chat={self.chat.pk}>'
