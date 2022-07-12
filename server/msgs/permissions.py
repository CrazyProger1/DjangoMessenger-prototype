from rest_framework import permissions
from chats.services import find_chat_members
from bots.extractors import extract_bot_from_request


class IsAuthenticatedOrBot(permissions.BasePermission):
    message = 'Authentication credentials were not provided.'

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        if request.bot:
            return True


class IsChatMember(permissions.BasePermission):
    message = 'You must be a member of the chat to perform this action.'

    def has_permission(self, request, view):
        chat_id = view.kwargs.get('chat_pk')

        if find_chat_members(user=request.user, chat=chat_id).first():
            return True

        if find_chat_members(bot=request.bot, chat=chat_id).first():
            return True
