# users/permissions.py
from rest_framework.permissions import BasePermission
from .utils import is_admin

class IsAdminOnly(BasePermission):
    """
    Allow access only to Admin users
    """
    def has_permission(self, request, view):
        return is_admin(request.user)
