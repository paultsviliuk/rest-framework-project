from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Custom permission to only allow superadmin access to it.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff  # TODO: change to is_superadmin

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff  # TODO: change to  is_superadmin
