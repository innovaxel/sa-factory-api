"""
This module defines URL patterns for user authentication in the Django application.

It includes the following routes:
- `register/`: Endpoint for user registration, handled by `UserRegistrationView`.
- `login/`: Endpoint for user login, handled by `LoginnView`.
"""
from __future__ import annotations

from django.urls import path

from accounts.views.authentication_views import LoginnView
from accounts.views.authentication_views import UpdatePinView
from accounts.views.authentication_views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginnView.as_view(), name='otp-login'),
    path('update-pin/', UpdatePinView.as_view(), name='update-pin'),
]