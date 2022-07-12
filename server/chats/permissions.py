from rest_framework import permissions, request as rq
from .services import *
from bots.extractors import extract_bot_from_request


class IsAuthenticatedOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        if request.bot:
            return True


class IsChatExists(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

            if chat:
                return True
        except models.ObjectDoesNotExist:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsChatOwnerOrChatIsPublicOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))

        if not chat.private:
            return True

        if chat.creator == request.user:
            return True


class IsChatFitOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            chat: Chat = get_chat_by_id(view.kwargs.get('chat_pk'))
        except models.ObjectDoesNotExist:
            return False

        if chat.group:
            return True

        members = get_chat_members_by_chat(chat)

        if not chat.group and len(members) < 2:
            return True


class IsInChatOrAddSelfOnly(permissions.BasePermission):
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
