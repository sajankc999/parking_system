from rest_framework import serializers

from .models import *

class ParkingSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpace
        fields = "__all__"

    def validate(self, attrs):
        if len(attrs['number'])<0 or len(attrs['number']>10):
            raise serializers.ValidationError
        return attrs
    
    

class Vehicle_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle_info
        fields = "__all__"

class ParkingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingDetails
        fields = "__all__"