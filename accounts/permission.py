from rest_framework.permissions import BasePermission
from .models import UserRole


class IsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            admin_role = UserRole.objects.get(user=request.user).role.name
        except UserRole.DoesNotExist:
            return False
        return admin_role.lower() == "admin"
