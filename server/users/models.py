from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, unique=True, verbose_name='user')
    # photo = models.ForeignKey('File', models.CASCADE, null=True, verbose_name='user photo')
    api_key = models.BinaryField(verbose_name='api key')

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return f'{self.user.username}'
