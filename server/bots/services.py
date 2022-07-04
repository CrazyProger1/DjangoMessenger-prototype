from .models import *


def get_all_bots():
    return Bot.objects.all()


def create_bot(*args, **kwargs) -> Bot:
    return Bot.objects.create(*args, **kwargs)
