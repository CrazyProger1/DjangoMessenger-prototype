from django.db import models
from django.contrib.auth.models import User


class Bot(models.Model):
    creator = models.ForeignKey(User, models.CASCADE, verbose_name='bot creator')
    name = models.CharField(verbose_name='bot name', max_length=200, unique=True)
    token = models.BinaryField(verbose_name='bot token')

    class Meta:
        verbose_name = 'Bot'
        verbose_name_plural = 'Bots'

    def __str__(self):
        return f'{self.name}'
