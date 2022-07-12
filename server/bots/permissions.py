from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'This action is only available to the owner.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.creator == request.user


class IsAuthenticatedOrBot(permissions.BasePermission):
    message = 'Authentication credentials were not provided.'

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            return True

        if request.bot:
            return True


class IsBot(permissions.BasePermission):
    message = 'This action is only available to the bots.'

    def has_permission(self, request, view):
        if request.bot:
            return True
