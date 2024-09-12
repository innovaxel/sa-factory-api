"""
This module contains views for user management in the Django application.

It includes:

1. `UserRegistrationView`: A view for handling user registration.
   - Handles user registration requests.
   - Validates and creates new users, handling errors such
        as validation errors and database integrity issues.

2. `LoginnView`: A view for handling user login.
   - Authenticates users based on API token and PIN.
   - Returns JWT tokens and user data upon successful authentication.
   - Handles errors such as non-existent devices and invalid PINs.
"""
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Devices
from accounts.models.user_devices import UserDevice
from accounts.serializers import LoginSerializer
from accounts.serializers import UpdatePinSerializer
from accounts.serializers import UserRegistrationSerializer


class UserRegistrationView(APIView):
    """
    View for handling user registration.

    Allows creating a new user by validating the input data
    and returning appropriate success or error responses.
    """

    def post(self, request):
        """
        Handle POST requests for user registration.

        Validates the input data, creates a new user if valid,
        and returns the appropriate response based on the outcome.

        Parameters:
            request: The HTTP request object containing user registration data.

        Returns:
            Response: A DRF Response object containing the
                        result of the registration process.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'User created successfully',
                    }, status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Validation failed',
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        except IntegrityError as e:
            error_message = 'Database integrity error'
            if 'unique constraint' in str(e).lower():
                if 'username' in str(e).lower():
                    error_message = 'Username already exists'
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': error_message,
                    'errors': str(e),
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as e:
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Validation error',
                    'errors': str(e),
                }, status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    """
    View for handling user login.

    Authenticates a user based on the provided API token and PIN.
    Returns JWT tokens and user data if authentication is successful.
    """

    def post(self, request):
        """
        Handle POST requests for user login.

        Validates the login data, checks the existence and linking of the device,
        and authenticates the user based on the PIN.

        Parameters:
            request: The HTTP request object containing login data.

        Returns:
            Response: A DRF Response object containing the result of the login process.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            api_token = serializer.validated_data['api_token']
            pin = serializer.validated_data['pin']

            try:
                device = Devices.objects.get(api_token=api_token)
            except Devices.DoesNotExist:
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device does not exist',
                        'data': {},
                    }, status=status.HTTP_404_NOT_FOUND,
                )

            try:
                user_device = UserDevice.objects.get(device=device)
                user = user_device.user
            except UserDevice.DoesNotExist:
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device is not linked to any user',
                        'data': {},
                    }, status=status.HTTP_404_NOT_FOUND,
                )

            if user.check_pin(pin):
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'Authentication successful',
                        'data': {
                            'user_data': {
                                'username': user.username,
                                'api_token': api_token,
                            },
                            'tokens': {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            },
                        },
                    }, status=status.HTTP_200_OK,
                )

            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid PIN',
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Validation failed',
                'data': {
                    'errors': serializer.errors,
                },
            }, status=status.HTTP_400_BAD_REQUEST,
        )


class UpdatePinView(APIView):
    """
    View for updating a user's PIN.

    Authenticates a user based on the JWT token, validates the provided API token,
    and updates the PIN if the device is linked to the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST requests for updating the user PIN.

        Parameters:
            request: The HTTP request object containing API token, new PIN, and JWT token.

        Returns:
            Response: A DRF Response object containing the
                        result of the PIN update process.
        """
        serializer = UpdatePinSerializer(data=request.data)
        if serializer.is_valid():
            api_token = serializer.validated_data['api_token']
            new_pin = serializer.validated_data['new_pin']

            user = request.user

            try:
                device = Devices.objects.get(api_token=api_token)
            except Devices.DoesNotExist:
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device does not exist',
                    }, status=status.HTTP_404_NOT_FOUND,
                )

            try:
                UserDevice.objects.get(device=device, user=user)
            except UserDevice.DoesNotExist:
                return Response(
                    {
                        'status_code': status.HTTP_403_FORBIDDEN,
                        'message': 'Device is not linked to the authenticated user',
                    }, status=status.HTTP_403_FORBIDDEN,
                )

            user.set_pin(new_pin)
            return Response(
                {
                    'status_code': status.HTTP_200_OK,
                    'message': 'PIN updated successfully',
                }, status=status.HTTP_200_OK,
            )

        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Validation failed',
                'data': {
                    'errors': serializer.errors,
                },
            }, status=status.HTTP_400_BAD_REQUEST,
        )
