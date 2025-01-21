import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import AdminModel
from rest_framework.permissions import BasePermission


class JWTAuthentication(permissions.BasePermission):
    """
    Custom permission class to authenticate a user based on JWT.
    """

    def has_permission(self, request, view):
        token = request.headers.get("AuthorizationToken")

        if not token or not token.startswith("Bearer "):
            return False

        try:
            # Decode the JWT token
            payload = jwt.decode(
                token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"]
            )
            request.user = (
                payload  # Attach the user information to the request
            )
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.DecodeError:
            return False
        except Exception:
            return False

    def get_response(self):
        return JsonResponse(
            {
                "success": False,
                "message": "AuthorizationToken token is required or invalid.",
            },
            status=401,
        )


class AdminJWTAuthentication(BasePermission):
    """
    Custom permission class to authenticate an admin user based on JWT.
    """

    def has_permission(self, request, view):
        # Extract token from the AuthorizationToken header
        token = request.headers.get("AuthorizationToken")

        if not token or not token.startswith("Bearer "):
            raise AuthenticationFailed("Authorization token is required.")

        try:
            # Decode the JWT token
            payload = jwt.decode(
                token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"]
            )

            # Attach the decoded user information to the request
            request.user = self.get_admin_from_payload(payload)

            # You can also validate the payload here, e.g., check for the presence of specific fields
            if "admin_id" not in payload:
                raise AuthenticationFailed("Invalid token: admin_id missing.")

            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid token.")
        except Exception as e:
            raise AuthenticationFailed(f"Error decoding token: {str(e)}")

    def get_admin_from_payload(self, payload):
        """
        Helper function to get the admin from the decoded payload using the custom AdminModel.
        """
        admin_id = payload.get("admin_id")
        try:
            # Fetch the admin user from the custom AdminModel
            admin = AdminModel.objects.get(id=admin_id)
            return admin
        except AdminModel.DoesNotExist:
            raise AuthenticationFailed("Admin not found.")
