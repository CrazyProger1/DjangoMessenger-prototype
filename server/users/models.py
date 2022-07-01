from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, models.CASCADE, unique=True, verbose_name='user')
    # photo = models.ForeignKey('File', models.CASCADE, null=True, verbose_name='user photo')
    api_key = models.BinaryField(verbose_name='api key')
    birthday_date = models.DateField(verbose_name='birthday date', null=True)

    class Meta:
        verbose_name = 'User profile'
        verbose_name_plural = 'User profiles'

    @staticmethod
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @staticmethod
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def __str__(self):
        return f'{self.user.username}'
