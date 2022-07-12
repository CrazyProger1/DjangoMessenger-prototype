from rest_framework import permissions, request as rq
from .services import *
from bots.extractors import extract_bot_from_request


class IsAuthenticatedOrBot(permissions.BasePermission):
    message = 'Authentication credentials were not provided.'

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        if request.bot:
            return True


class IsChatExists(permissions.BasePermission):
    message = 'Chat with that id is not exists.'

    def has_permission(self, request, view):
        try:
            chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

            if chat:
                return True
        except models.ObjectDoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'This action is only available to the owner.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsChatOwnerOrChatIsPublicOrReadOnly(permissions.BasePermission):
    message = 'This action is only available to the owner.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

        if not chat.private:
            return True

        if chat.creator == request.user:
            return True


class IsChatFitOrReadOnly(permissions.BasePermission):
    message = 'This is not a group chat, the maximum number of members is 2.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

        if chat.group:
            return True

        members = get_chat_members_by_chat(chat)

        if not chat.group and len(members) < 2:
            return True


class IsInChatOrAddSelfOnly(permissions.BasePermission):
    message = 'You must be a member of the chat to add other.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

        user_to_add_pk = request.data.get('user')
        request_user = request.user

        # checks if in chat
        user_chat_member = find_chat_members(user=request_user, chat=chat).first()

        if user_chat_member:
            return True

        # checks if user adds self
        if user_to_add_pk is not None:
            if request.method == 'POST' \
                    and view.kwargs.get('pk') is None \
                    and user_to_add_pk == request_user.pk:
                return True
