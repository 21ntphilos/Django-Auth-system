import secrets
from rest_framework import generics
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import throttling
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

User = get_user_model()

class UserRegisterRateThrottle(throttling.AnonRateThrottle):
    scope = "register"

class UserLoginRateThrottle(throttling.AnonRateThrottle):
    scope = "login"

class UserResetPasswordRateThrottle(throttling.AnonRateThrottle):
    scope = "reset"

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAccountSerializer

class LoginView(TokenObtainPairView):
    throttle_classes = [UserLoginRateThrottle]

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
    
        if user:
            token = secrets.token_urlsafe(30)
            settings.REDIS_CLIENT.set(f"reset_token:{token}", user.id, ex=600)

            reset_link = f"http://localhost:8000/api/account/reset-password/?token={token}"

            return Response({"message": "Password reset link has been sent to your email.", "reset_link": reset_link},status=status.HTTP_200_OK)

        return Response({"message": "If this email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    throttle_classes = [UserResetPasswordRateThrottle]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response(
                {"error": "Token and new password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = settings.REDIS_CLIENT.get(f"reset_token:{token}")
        
        if not user_id:
            return Response(
            {"error": "Invalid or expired token."},
            status=status.HTTP_400_BAD_REQUEST,
        )

        
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()

                settings.REDIS_CLIENT.delete(f"reset_token:{token}")

                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Invalid token or user does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
