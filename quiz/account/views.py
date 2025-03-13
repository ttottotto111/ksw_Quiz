from django.shortcuts import render
from rest_framework import generics

from .serializers import UserSerializer, AdminSerializer
from django.contrib.auth.models import User

# Create your views here.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class AdminCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AdminSerializer