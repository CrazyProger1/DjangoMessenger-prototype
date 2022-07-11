from rest_framework import permissions
from chats.services import find_chat_members
from bots.extractors import extract_bot_from_request


class IsAuthenticatedOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        token = request.headers.get('BotAuthorization', False)
        if token:
            bot = extract_bot_from_request(request)

            if bot:
                view.kwargs.update({'bot': bot})
                return True


class IsChatMember(permissions.BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get('chat_pk')

        if find_chat_members(user=request.user, chat=chat_id).first():
            return True

        if find_chat_members(bot=view.kwargs.get('bot'), chat=chat_id).first():
            return True
