# # backends.py
# from django.contrib.auth.backends import BaseBackend
# from .models import HumanResource


# class HumanResourceBackend(BaseBackend):
#     def authenticate(self, request, hr_guid=None, hr_pin=None, **kwargs):
#         try:
#             user = HumanResource.objects.get(hr_guid=hr_guid, hr_pin=hr_pin)
#             return user
#         except HumanResource.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return HumanResource.objects.get(pk=user_id)
#         except HumanResource.DoesNotExist:
#             return None


# backends.py
from django.contrib.auth.backends import BaseBackend
from .models import HumanResource


class HumanResourceBackend(BaseBackend):
    def authenticate(self, request, hr_guid=None, hr_pin=None, **kwargs):
        try:
            user = HumanResource.objects.get(hr_guid=hr_guid, hr_pin=hr_pin)
            return user
        except HumanResource.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return HumanResource.objects.get(pk=user_id)
        except HumanResource.DoesNotExist:
            return None
