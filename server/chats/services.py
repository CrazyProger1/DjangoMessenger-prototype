from .models import *
from typing import Iterable


def get_all_chats():
    return Chat.objects.all()


def get_all_chat_members():
    return ChatMember.objects.all()


def get_chat_members_by_chat_id(chat_id: int):
    return ChatMember.objects.filter(chat=chat_id)


def get_chat_members_by_chat(chat: Chat):
    return ChatMember.objects.filter(chat=chat)


def get_chat_by_id(chat_id: int, ignore_errors: bool = False):
    if not ignore_errors:
        return Chat.objects.get(pk=chat_id)

    return Chat.objects.filter(pk=chat_id)


def find_chat_members(**kwargs) -> Iterable[ChatMember]:
    return ChatMember.objects.filter(**kwargs)
