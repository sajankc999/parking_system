from rest_framework import serializers

from REST_API.models import *

"""
Class serializer for ParkingSpace.
"""


class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = "__all__"

    def validate(self, attrs):
        number = attrs["number"]
        if (number) < 0 or (number > 10):
            raise serializers.ValidationError
        return attrs


"""
Class Serializer for vehicel info.

"""


class Vehicle_infoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vehicle_info
        fields = "__all__"


"""

Class serializer for parking details.

"""


class ParkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = "__all__"
