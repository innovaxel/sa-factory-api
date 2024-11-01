# """
# This module defines URL patterns for user authentication in the Django application.

# It includes the following routes:
# - `register/`: Endpoint for user registration, handled by `UserRegistrationView`.
# - `login/`: Endpoint for user login, handled by `LoginnView`.
# """
# from __future__ import annotations

# from django.urls import path

# from accounts.views.authentication_views import (
#     AdminLoginView,
#     LoginView,
#     UpdatePinView,
#     DeviceRegistrationView,
#     SetPinView,
#     LogoutView,
# )

# urlpatterns = [
#     path('device-register/', DeviceRegistrationView.as_view(), name='device-register'),
#     path('login/', LoginView.as_view(), name='otp-login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('admin-login/', AdminLoginView.as_view(), name='admin-login'),
#     path('update-pin/', UpdatePinView.as_view(), name='update-pin'),
#     path('set-pin/', SetPinView.as_view(), name='set-pin'),
# ]


# urls.py
from django.urls import path
from .views import LoginView, UserProfileView, UpdateHRPinView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("set-pin/", UpdateHRPinView.as_view(), name="set-pin"),
    # path("profile/", UserProfileView.as_view(), name="user_profile"),
]
