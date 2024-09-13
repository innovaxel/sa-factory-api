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

from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Devices
from accounts.models.user_devices import UserDevice
from accounts.serializers import DevicesSerializer
from accounts.serializers import LoginSerializer
from accounts.serializers import UpdatePinSerializer
from accounts.serializers import UserDeviceSerializer
from accounts.serializers import UserRegistrationInputSerializer
from accounts.serializers import UserSerializer


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

        # Check if the device already exists
        if Devices.objects.filter(api_key=api_key).exists() or \
           Devices.objects.filter(device_id=device_id).exists() or \
           Devices.objects.filter(api_url=api_url).exists():
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Device already exists with the\
                          provided api_key, device_id, or api_url',
                    'data': {},
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the device
        device_data = {
            'api_key': api_key,
            'device_id': device_id,
            'api_url': api_url,
        }
        device_serializer = DevicesSerializer(data=device_data)
        if device_serializer.is_valid():
            device = device_serializer.save()
        else:
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Device creation failed',
                    'data': device_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the user
        user_data = {
            'full_name': full_name,
            'pin': pin,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            try:
                user = user_serializer.save()
            except IntegrityError as e:
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'User creation failed',
                        'data': {'detail': str(e)},
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User creation failed',
                    'data': user_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        # Link the user and the device
        user_device_data = {
            'user': user.id,
            'device': device.id,
        }
        user_device_serializer = UserDeviceSerializer(data=user_device_data)
        if user_device_serializer.is_valid():
            user_device_serializer.save()
        else:
            return Response(
                {
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Failed to link user and device',
                    'data': user_device_serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'status_code': status.HTTP_201_CREATED,
                'message': 'Device Registration Successfully',
            }, status=status.HTTP_201_CREATED,
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
            api_key = serializer.validated_data['api_key']
            pin = serializer.validated_data['pin']

            try:
                device = Devices.objects.get(api_key=api_key)
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

            if user.pin:
                if user.check_pin(pin):
                    refresh = RefreshToken.for_user(user)
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
                return Response(
                    {
                        'status_code': status.HTTP_400_BAD_REQUEST,
                        'message': 'Invalid PIN',
                    }, status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                # If PIN is empty, set the PIN and then authenticate
                user.set_pin(pin)
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'PIN set and authentication successful',
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

                return Response(
                    {
                        'status_code': status.HTTP_200_OK,
                        'message': 'PIN updated successfully',
                        'data': DevicesSerializer(device).data,
                    }, status=status.HTTP_200_OK,
                )
            except Devices.DoesNotExist:
                return Response(
                    {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'message': 'Device not found',
                    }, status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Invalid input',
                'data': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST,
        )
