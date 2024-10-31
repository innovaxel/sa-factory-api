from rest_framework import serializers
from accounts.models import HumanResource


class HumanResourceSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    pin_set = serializers.SerializerMethodField()

    class Meta:
        model = HumanResource
        fields = [
            "id",
            "pin",
            "pin_set",
        ]

    id = serializers.CharField(source="hr_guid")
    pin = serializers.CharField(source="hr_pin")

    def get_pin_set(self, obj):
        """
        Custom method to get the value for the `pin_set` field.w
        """
        return obj.hr_pin is not None and obj.hr_pin != ""
