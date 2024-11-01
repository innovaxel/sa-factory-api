import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import permissions


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
