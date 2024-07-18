from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import generics
from .serializer import *
from rest_framework.permissions import AllowAny
from .tasks import send_welcome_email
from rest_framework.response import Response
User = get_user_model()

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            send_welcome_email.delay_on_commit(serializer.validated_data['email'])
            if user.objects.filter(username=serializer.validated_data['username']).first():
                return serializers.ValidationError('user exists')
            User= user.objects.create(username=serializer.validated_data['username'],password=make_password(serializer.validated_data['password']))
            return Response('user Created')



    
