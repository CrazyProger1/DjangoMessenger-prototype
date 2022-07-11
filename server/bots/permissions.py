from rest_framework import permissions
from .extractors import *


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsAuthenticatedOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        token = request.headers.get('BotAuthorization', False)
        if token:
            bot = extract_bot(request)
            return bot is not None
