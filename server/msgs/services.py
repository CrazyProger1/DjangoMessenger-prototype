from .models import *


def get_all_messages():
    return Message.objects.all()


def get_messages_by_chat_id(chat_id: int):
    return Message.objects.filter(chat=chat_id)


def get_unread_messages(chat_id: int, last_read_id: int):
    return Message.objects.filter(chat=chat_id, pk__gte=last_read_id)
