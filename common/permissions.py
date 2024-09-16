from rest_framework.permissions import BasePermission
from accounts.models import SimpleUser

class IsSimpleUserOrAdmin(BasePermission):
    def has_permission(self, request, view):
        print("*********AAAA*********")
        print("**********************")
        print("User: ", request.user)
        user = request.user
        if isinstance(user, SimpleUser) or (user.is_authenticated and user.is_staff):
            return True
        return False

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        print("**********************")
        print("**********************")
        print("**********************")
        print("**********************")
        print("**********************")

        user = request.user
        if user.is_authenticated and user.is_staff:
            return True
        return False
