from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer