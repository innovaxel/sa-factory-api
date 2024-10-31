# """
# This module contains views for user management in the Django application.

# It includes:

# 1. `UserRegistrationView`: A view for handling user registration.
#    - Handles user registration requests.
#    - Validates and creates new users, handling errors such
#         as validation errors and database integrity issues.

# 2. `LoginnView`: A view for handling user login.
#    - Authenticates users based on API token and PIN.
#    - Returns JWT tokens and user data upon successful authentication.
#    - Handles errors such as non-existent devices and invalid PINs.
# """
# from __future__ import annotations

# import logging

# from django.contrib.auth.hashers import make_password
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from django.core.exceptions import ObjectDoesNotExist
# from accounts.permission import IsAdminOnly
# from common.device_validator import DeviceValidator

# from accounts.models import (
#     Devices,
#     SimpleUser,
#     UserDevice,
# )

# from accounts.serializers import (
#     AdminLoginSerializer,
#     DevicesSerializer,
#     UpdatePinSerializer,
#     DeviceAuthenticationSerializer,
#     DeviceRegistrationInputSerializer,
#     SetPinSerializer,
#     SimpleUserSerializer,
# )

# from rest_framework_simplejwt.token_blacklist.models import (
#     BlacklistedToken,
#     OutstandingToken,
# )


# logger = logging.getLogger('accounts')


# class DeviceRegistrationView(APIView):
#     """
#     Handles the device registration process.
#     """

#     permission_classes = [IsAdminOnly]

#     def post(self, request):
#         """
#         Processes the device registration request by validating input data
#         and creating a device if it does not already exist.
#         """

#         input_serializer = DeviceRegistrationInputSerializer(data=request.data)
#         if not input_serializer.is_valid():
#             logger.error('Invalid input data: %s', input_serializer.errors)
#             return Response(
#                 {
#                     'message': 'Invalid input data',
#                     'errors': input_serializer.errors,
#                 }, status=status.HTTP_400_BAD_REQUEST,
#             )

#         api_key = input_serializer.validated_data['api_key']
#         device_id = input_serializer.validated_data['device_id']
#         api_url = input_serializer.validated_data['api_url']

#         device_id_exists = Devices.objects.filter(device_id=device_id).exists()
#         api_key_exists = Devices.objects.filter(api_key=api_key).exists()

#         if device_id_exists or api_key_exists:
#             errors = {}
#             if device_id_exists:
#                 errors['device_id'] = 'Device with this device_id already exists.'
#             if api_key_exists:
#                 errors['api_key'] = 'Device with this api_key already exists.'

#             logger.error('Device registration failed due to conflicts: %s', errors)
#             return Response(
#                 {
#                     'message': 'Device registration failed',
#                     'errors': errors,
#                 }, status=status.HTTP_400_BAD_REQUEST,
#             )

#         device_data = {
#             'api_key': api_key,
#             'device_id': device_id,
#             'api_url': api_url,
#         }
#         device_serializer = DevicesSerializer(data=device_data)
#         if device_serializer.is_valid():
#             device = device_serializer.save()
#             logger.info('Device created successfully: %s', device.device_id)
#         else:
#             logger.error('Device creation failed: %s', device_serializer.errors)
#             return Response(
#                 {
#                     'message': 'Device creation failed',
#                     'errors': device_serializer.errors,
#                 }, status=status.HTTP_400_BAD_REQUEST,
#             )

#         logger.info('Device registration successful: %s', device.device_id)
#         return Response(
#             {
#                 'message': 'Device registration successful',
#             }, status=status.HTTP_201_CREATED,
#         )


# class UpdatePinView(APIView):
#     """
#     API view for updating the PIN of a device.

#     This view handles POST requests to update the
#     PIN for a device identified by its API key.
#     """
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Handle POST request to update the PIN of a device.

#         Validates the request data, checks if the device
#         exists, updates its PIN, and returns
#         a success response or an error response if the device
#         is not found or the input is invalid.

#         Args:
#             request (Request): The request object
#             containing the data to be processed.

#         Returns:
#             Response: A response object containing the status
#             code, message, and any relevant data.
#         """
#         device_id = request.data.get('device_id')

#         validator = DeviceValidator(device_id)
#         response = validator.validate()
#         if response:
#             return response

#         serializer = UpdatePinSerializer(data=request.data)
#         if serializer.is_valid():
#             api_key = serializer.validated_data['api_key']
#             new_pin = serializer.validated_data['new_pin']

#             try:
#                 device = Devices.objects.get(api_key=api_key)
#                 device.api_key = new_pin
#                 device.save()

#                 logger.info('PIN updated successfully for device: %s', device.device_id)
#                 return Response(
#                     {
#                         'message': 'PIN updated successfully',
#                         'data': DevicesSerializer(device).data,
#                     }, status=status.HTTP_200_OK,
#                 )
#             except Devices.DoesNotExist:
#                 logger.error('Device not found: %s', api_key)
#                 return Response(
#                     {
#                         'message': 'Device not found',
#                     }, status=status.HTTP_404_NOT_FOUND,
#                 )

#         logger.error('Invalid input data: %s', serializer.errors)
#         return Response(
#             {
#                 'message': 'Invalid input',
#                 'errors': serializer.errors,
#             }, status=status.HTTP_400_BAD_REQUEST,
#         )


# class AdminLoginView(APIView):
#     """
#     View for admin login, handling authentication and token generation.
#     """
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Handle POST requests for admin login. Authenticates
#         the user and generates JWT tokens.
#         """
#         serializer = AdminLoginSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data['username']
#             password = serializer.validated_data['password']
#             user = authenticate(username=username, password=password)

#             if user and user.is_staff:
#                 refresh = RefreshToken.for_user(user)
#                 tokens = {
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }

#                 logger.info('Admin with username %s authenticated successfully', username)
#                 return Response(
#                     {
#                         'message': 'Authenti cation successful',
#                         'tokens': tokens,
#                     }, status=status.HTTP_200_OK,
#                 )
#             else:
#                 logger.error('Invalid credentials or user is not an admin.')
#                 return Response(
#                     {
#                         'message': 'Invalid credentials or user is not an admin.',
#                         'data': None,
#                     }, status=status.HTTP_400_BAD_REQUEST,
#                 )
#         logger.error('Invalid data: %s', serializer.errors)
#         return Response(
#             {
#                 'message': 'Invalid Credentials',
#                 'errors': serializer.errors,
#             }, status=status.HTTP_400_BAD_REQUEST,
#         )


# class LoginView(APIView):
#     """
#     API view to authenticate a SimpleUser based on device ID and PIN.
#     """

#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Handle POST request for user authentication.

#         Args:
#             request (Request): The request object containing device_id and pin.

#         Returns:
#             Response: A response containing status code, message, user, and tokens.
#         """
#         serializer = DeviceAuthenticationSerializer(data=request.data)

#         if serializer.is_valid():
#             device_id = serializer.validated_data['device_id']
#             pin = serializer.validated_data['pin']

#             try:
#                 device = Devices.objects.get(device_id=device_id)
#             except Devices.DoesNotExist:
#                 return Response(
#                     {
#                         'message': 'Device not found.',
#                         'errors': {
#                             'device': 'Device not found.',
#                         },
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             try:
#                 user_device = UserDevice.objects.get(device=device)
#                 user = user_device.user
#                 logger.error('Invalid data.zzzzzzzzzzzz')
#             except UserDevice.DoesNotExist:
#                 return Response(
#                     {
#                         'message': 'No user associated with this device.',
#                         'errors': {
#                             'device': 'No user associated with this device.',
#                         },
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if not isinstance(user, SimpleUser):
#                 return Response(
#                     {
#                         'message': 'Invalid user type.',
#                         'errors': {
#                             'user': 'Invalid user type.',
#                         },
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             if pin != user.pin:
#                 return Response(
#                     {
#                         'message': 'Invalid PIN.',
#                         'errors': {
#                             'pin': 'Invalid PIN.',
#                         },
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             logger.info('User authenticated successfully: %s', user.full_name)
#             refresh = RefreshToken.for_user(user)
#             access_token = str(refresh.access_token)
#             refresh_token = str(refresh)

#             return Response(
#                 {
#                     'message': 'Authentication successful',
#                     'data': {
#                         'user': SimpleUserSerializer(user).data,
#                         'tokens': {
#                             'access': access_token,
#                             'refresh': refresh_token,
#                         },
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         return Response(
#             {
#                 'message': 'Validation failed',
#                 'errors': serializer.errors,
#             },
#             status=status.HTTP_400_BAD_REQUEST,
#         )


# class SetPinView(APIView):
#     """
#     API view to set the PIN for a `SimpleUser`.

#     It checks if the device exists, verifies the
#     user-device link, and sets the PIN if not already set.
#     """
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """
#         Handles the request to set the PIN for a user, after
#         validating the device and user link.
#         """
#         serializer = SetPinSerializer(data=request.data)
#         if not serializer.is_valid():
#             logger.error('Invalid input data: %s', serializer.errors)
#             return Response(
#                 {
#                     'message': 'Invalid input data',
#                     'data': serializer.errors,
#                 }, status=status.HTTP_400_BAD_REQUEST,
#             )

#         pin = serializer.validated_data['pin']
#         device_id = serializer.validated_data['device_id']
#         user_id = serializer.validated_data['user_id']

#         try:
#             device = Devices.objects.get(device_id=device_id)
#         except Devices.DoesNotExist:
#             logger.error('Device with ID %s does not exist', device_id)
#             return Response(
#                 {
#                     'message': 'Device not found',
#                 }, status=status.HTTP_404_NOT_FOUND,
#             )

#         try:
#             user_device = UserDevice.objects.get(device=device, user__id=user_id)
#             user = user_device.user
#         except UserDevice.DoesNotExist:
#             logger.error(
#                 'User with ID %s is not linked to device with ID %s', user_id, device_id,
#             )
#             return Response(
#                 {
#                     'message': 'User is not linked to this device',
#                 }, status=status.HTTP_401_UNAUTHORIZED,
#             )

#         if user.pin:
#             return Response(
#                 {
#                     'message': 'PIN is already set',
#                 }, status=status.HTTP_400_BAD_REQUEST,
#             )

#         user.pin = pin
#         user.password = make_password(pin)
#         user.save()

#         logger.info('PIN set successfully for user: %s', user.username)
#         return Response(
#             {
#                 'message': 'PIN set successfully',
#                 'data': SimpleUserSerializer(user).data,
#             }, status=status.HTTP_200_OK,
#         )


# class LogoutView(APIView):
#     """
#     API view to log out a SimpleUser by blacklisting their refresh token.
#     """
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         """
#         Handles the logout request by blacklisting the user's refresh token.

#         Args:
#             request (Request): The request object containing the user's refresh token.

#         Returns:
#             Response: A response indicating the logout success or failure.
#         """
#         user = request.user

#         refresh_token = request.data.get('refresh_token')
#         if not refresh_token:
#             return Response(
#                 {
#                     'message': 'Refresh token is required.',
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             outstanding_token = OutstandingToken.objects.get(token=refresh_token)

#             BlacklistedToken.objects.create(token=outstanding_token)

#             logger.info('User logged out successfully: %s', user.username)
#             return Response(
#                 {
#                     'message': 'Logout successful.',
#                 },
#                 status=status.HTTP_205_RESET_CONTENT,
#             )
#         except ObjectDoesNotExist:
#             logger.error('Invalid refresh token for user: %s', user.username)
#             return Response(
#                 {
#                     'message': 'Invalid refresh token.',
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from accounts.models import HumanResource
from accounts.serializers import HumanResourceAuthSerializer


class HumanResourceAuthView(APIView):
    def post(self, request):
        serializer = HumanResourceAuthSerializer(data=request.data)

        if serializer.is_valid():
            hr_guid = serializer.validated_data["hr_guid"]
            pin = serializer.validated_data["hr_pin"]

            try:
                # Retrieve the user based on hr_guid
                user = HumanResource.objects.get(hr_guid=hr_guid)

                # Check the pin
                if not check_password(pin, user.hr_pin):
                    return Response(
                        {
                            "message": "Invalid PIN.",
                            "errors": {
                                "pin": "Invalid PIN.",
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Generate tokens (using a method or library of your choice)
                refresh = RefreshToken.for_user(
                    user
                )  # Assuming you have token logic in place
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response(
                    {
                        "message": "Authentication successful",
                        "data": {
                            "user": HumanResourceSerializer(user).data,
                            "tokens": {
                                "access": access_token,
                                "refresh": refresh_token,
                            },
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            except HumanResource.DoesNotExist:
                return Response(
                    {
                        "message": "Invalid user ID.",
                        "errors": {
                            "hr_guid": "User does not exist.",
                        },
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {
                "message": "Validation failed",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
