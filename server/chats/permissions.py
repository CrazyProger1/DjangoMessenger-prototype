from rest_framework import permissions, request as rq
from .services import *


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsChatOwnerOrChatIsPublicOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            chat: Chat = get_chat_by_id(view.kwargs.get('pk'))
        except models.ObjectDoesNotExist:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not chat.private:
            return True

        if chat.creator == request.user:
            return True
