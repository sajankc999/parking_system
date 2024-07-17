from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

user = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields =['username','password']
        extra_kwargs ={"password":{"write_only":True}}
    def create(self, validated_data):
        if user.objects.filter(username=validated_data['username']).first():
            return serializers.ValidationError('user exists')
        User= user.objects.create(username=validated_data['username'],password=make_password(validated_data['password']))
        return User