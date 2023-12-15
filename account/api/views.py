from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer


class UserListSerializer(generics.ListAPIView): # read only
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailSerializer(generics.RetrieveAPIView): # read only
    queryset = User.objects.all()
    serializer_class = UserSerializer