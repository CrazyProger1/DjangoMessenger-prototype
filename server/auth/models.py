from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    user = models.ForeignKey(User, models.CASCADE)
    photo = models.ForeignKey('Photo', models.CASCADE)
    api_key = models.BinaryField('Api key')

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    def __str__(self):
        return f'{self.user.username} profile'
