from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import generics
from .serializer import *
from rest_framework.permissions import AllowAny
User = get_user_model()

class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    
