from django.db import models
from msgs.models import Message


class File(models.Model):
    name = models.CharField(verbose_name='file name', max_length=200)
    link = models.CharField(verbose_name='clouded file link', max_length=200)
    message = models.ForeignKey(Message, models.CASCADE)
    encryption_type = models.CharField(verbose_name='file encryption', max_length=10, default='AES')
