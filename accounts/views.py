from rest_framework import generics
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class UserAccountView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer