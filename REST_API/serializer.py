from rest_framework import serializers

from .models import *

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = "__all__"

class Vehicle_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_info
        fields = "__all__"

class ParkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = "__all__"