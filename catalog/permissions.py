from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows full access to admins, read-only to others.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff


class IsAuthenticatedAdmin(BasePermission):
    """
    Only allows access to authenticated admin/staff users.
    Requires authentication and admin privileges for all operations.
    """

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_staff
        )
