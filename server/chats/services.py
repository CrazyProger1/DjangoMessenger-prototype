from .models import *


def get_all_chats():
    return Chat.objects.all()


def get_all_chat_members():
    return ChatMember.objects.all()


def get_chat_members_by_chat_id(chat_id: int):
    return ChatMember.objects.filter(chat=chat_id)
