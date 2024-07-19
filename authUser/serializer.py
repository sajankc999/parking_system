from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

user = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}
