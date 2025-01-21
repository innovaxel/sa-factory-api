from django.contrib.auth.backends import BaseBackend
from .models import HumanResource, AdminModel


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


class AdminBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            admin = AdminModel.objects.get(username=username)
            if admin.check_password(password):
                return admin
        except AdminModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return AdminModel.objects.get(pk=user_id)
        except AdminModel.DoesNotExist:
            return None
