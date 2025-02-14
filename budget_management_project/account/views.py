from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegisterSerializer


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
