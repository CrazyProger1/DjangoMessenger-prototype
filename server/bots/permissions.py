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
            bot = extract_bot_from_request(request)

            if bot:
                view.kwargs.update({'bot': bot})
                return True


class IsBot(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('BotAuthorization', False)
        if token:
            bot = extract_bot_from_request(request)

            if bot:
                view.kwargs.update({'bot': bot})
                return True
