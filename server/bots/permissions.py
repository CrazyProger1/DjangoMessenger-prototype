from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsAuthenticatedOrBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        if request.bot:
            return True


class IsBot(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.bot:
            return True
