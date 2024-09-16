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

import logging

from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import (
    Devices,
    SimpleUser,
    UserDevice,
)
from accounts.serializers import (
    AdminLoginSerializer,
    DevicesSerializer,
    LoginSerializer,
    UpdatePinSerializer,
    UserDeviceSerializer,
    UserRegistrationInputSerializer,
    UserSerializer,
)

logger = logging.getLogger('accounts')


class UserRegistrationView(APIView):
    """
    Handles the user registration process, including device creation,
    user creation, and linking the user to the device.
    """

    def post(self, request):
        """
        Processes the registration request by validating input data,
        creating a device, creating a user, and linking the user to the device.
        """

        input_serializer = UserRegistrationInputSerializer(data=request.data)
        if not input_serializer.is_valid():

            logger.error('Invalid input data: %s', input_serializer.errors)
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Invalid input data',
                    'data': input_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        api_key = input_serializer.validated_data['api_key']
        device_id = input_serializer.validated_data['device_id']
        api_url = input_serializer.validated_data['api_url']
        full_name = input_serializer.validated_data['full_name']
        pin = input_serializer.validated_data.get('pin', '')

        if Devices.objects.filter(api_key=api_key).exists() or \
           Devices.objects.filter(device_id=device_id).exists() or \
           Devices.objects.filter(api_url=api_url).exists():

            logger.error(
                'Device already exists with'
                'the provided api_key, device_id, or api_url',
            )
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Device already exists with the\
                          provided api_key, device_id, or api_url',
                    'data': {},
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        device_data = {
            'api_key': api_key,
            'device_id': device_id,
            'api_url': api_url,
        }
        device_serializer = DevicesSerializer(data=device_data)
        if device_serializer.is_valid():
            device = device_serializer.save()
        else:
            logger.error('Device creation failed: %s', device_serializer.errors)
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Device creation failed',
                    'data': device_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        user_data = {
            'full_name': full_name,
            'pin': pin,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
                logger.info('User created successfully: %s', user.full_name)
            except IntegrityError as e:
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'User creation failed',
                        'data': {'detail': str(e)},
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            logger.error('User creation failed: %s', user_serializer.errors)
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User creation failed',
                    'data': user_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        user_device_data = {
            'user': user.id,
            'device': device.id,
        }
        user_device_serializer = UserDeviceSerializer(data=user_device_data)
        if user_device_serializer.is_valid():
            user_device_serializer.save()
        else:
            logger.error(
                'Failed to link user and device: '
                '%s', user_device_serializer.errors,
            )
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Failed to link user and device',
                    'data': user_device_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        logger.info('User registration successful: %s', user.full_name)
        return Response(
            {
                'status_code': status.HTTP_201_CREATED,
                'message': 'Device Registration Successfully',
            }, status=status.HTTP_201_CREATED,
        )


class UpdatePinView(APIView):
    """
    API view for updating the PIN of a device.

    This view handles POST requests to update the
    PIN for a device identified by its API key.
    """

    def post(self, request):
        """
        Handle POST request to update the PIN of a device.

        Validates the request data, checks if the device
        exists, updates its PIN, and returns
        a success response or an error response if the device
        is not found or the input is invalid.

        Args:
            request (Request): The request object
            containing the data to be processed.

        Returns:
            Response: A response object containing the status
            code, message, and any relevant data.
        """
        serializer = UpdatePinSerializer(data=request.data)
        if serializer.is_valid():
            api_key = serializer.validated_data['api_key']
            new_pin = serializer.validated_data['new_pin']

            try:
                device = Devices.objects.get(api_key=api_key)
                device.api_key = new_pin
                device.save()

                logger.info('PIN updated successfully for device: %s', device.device_id)
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'PIN updated successfully',
                        'data': DevicesSerializer(device).data,
                    }, status=status.HTTP_200_OK,
                )
            except Devices.DoesNotExist:
                logger.error('Device not found: %s', api_key)
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device not found',
                    }, status=status.HTTP_404_NOT_FOUND,
                )

        logger.error('Invalid input data: %s', serializer.errors)
        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid input',
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST,
        )


class AdminLoginView(APIView):
    """
    View for admin login, handling authentication and token generation.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests for admin login. Authenticates
        the user and generates JWT tokens.
        """
        serializer = AdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user and user.is_staff:
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                logger.info('Admin with username %s authenticated successfully', username)
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'Authenti cation successful',
                        'tokens': tokens,
                    }, status=status.HTTP_200_OK,
                )
            else:
                logger.error('Invalid credentials or user is not an admin.')
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid credentials or user is not an admin.',
                        'data': None,
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        logger.error('Invalid data: %s', serializer.errors)
        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid data.',
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    """
    View for handling login requests with API key and PIN authentication.
    """

    def post(self, request):
        """
        Handle POST requests for user login. Authenticates
        the user and generates JWT tokens.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            api_key = serializer.validated_data['api_key']
            pin = serializer.validated_data['pin']

            try:
                device = Devices.objects.get(api_key=api_key)
                logger.info('Device found: %s', device.device_id)
            except Devices.DoesNotExist:
                logger.error('Device does not exist')
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
                logger.info('User found: %s', user.full_name)
            except UserDevice.DoesNotExist:
                logger.error('Device is not linked to any user')
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device is not linked to any user',
                        'data': {},
                    }, status=status.HTTP_404_NOT_FOUND,
                )

            if isinstance(user, SimpleUser):
                if user.check_pin(pin):
                    refresh = RefreshToken.for_user(user)
                    logger.info(
                        'User authenticated with name: %s '
                        'authentication successful', user.full_name,
                    )
                    return Response(
                        {
                            'status_code': status.HTTP_200_OK,
                            'message': 'Authentication successful',
                            'data': {
                                'user_data': {
                                    'full_name': user.full_name,
                                    'api_key': api_key,
                                },
                                'tokens': {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                },
                            },
                        }, status=status.HTTP_200_OK,
                    )
                else:
                    logger.error('Invalid PIN')
                    return Response(
                        {
                            'status_code': status.HTTP_400_BAD_REQUEST,
                            'message': 'Invalid PIN',
                        }, status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                logger.error('User is not recognized')
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'User is not recognized',
                    }, status=status.HTTP_400_BAD_REQUEST,
                )

        logger.error('Validation failed: %s', serializer.errors)
        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Validation failed',
                'data': {
                    'errors': serializer.errors,
                },
            }, status=status.HTTP_400_BAD_REQUEST,
        )
