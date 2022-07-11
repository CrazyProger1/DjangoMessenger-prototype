from .models import *


def get_all_bots():
    return Bot.objects.all()


def create_bot(*args, **kwargs) -> Bot:
    return Bot.objects.create(*args, **kwargs)


def get_bot_by_token(token):
    try:
        return Bot.objects.get(token=token)
    except Exception as e:
        print(e)
        return None
