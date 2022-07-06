from .models import *


def get_all_chats():
    return Chat.objects.all()
