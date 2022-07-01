from django.contrib.auth.models import User


def get_all_users():
    return User.objects.all()
