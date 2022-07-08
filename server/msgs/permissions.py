from rest_framework import permissions
from chats.services import find_chat_members


class IsChatMember(permissions.BasePermission):
    def has_permission(self, request, view):
        if find_chat_members(user=request.user, chat=view.kwargs.get('chat_pk')).first():
            return True
