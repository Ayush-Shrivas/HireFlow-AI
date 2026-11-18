import json
import secrets
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, RegisterSerializer, UserSerializer


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"refresh": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            return Response({"refresh": ["Invalid or expired refresh token."]}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email=serializer.validated_data["email"], is_active=True).first()
        response = {"detail": "If an account exists, password reset instructions have been prepared."}
        if user and settings.DEBUG:
            response.update({"uid": urlsafe_base64_encode(force_bytes(user.pk)), "token": default_token_generator.make_token(user)})
        return Response(response)


class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(pk=force_str(urlsafe_base64_decode(serializer.validated_data["uid"])))
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"detail": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, serializer.validated_data["token"]):
            return Response({"detail": "Invalid or expired reset link."}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data["password"])
        user.save(update_fields=("password", "updated_at"))
        return Response({"detail": "Password updated successfully."})
import json
import secrets
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect


class GoogleLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            return Response({"detail": "Google sign-in is not configured."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        state = secrets.token_urlsafe(32)
        request.session["google_oauth_state"] = state
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "online",
            "prompt": "select_account",
            "state": state,
        }
        return HttpResponseRedirect("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params))


class GoogleCallbackView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from rest_framework_simplejwt.tokens import RefreshToken

        if request.query_params.get("state") != request.session.pop("google_oauth_state", None):
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/login?error=google_state")
        code = request.query_params.get("code")
        if not code:
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/login?error=google_cancelled")
        try:
            token_request = urllib.request.Request(
                "https://oauth2.googleapis.com/token",
                data=urllib.parse.urlencode({
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }).encode(),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with urllib.request.urlopen(token_request, timeout=10) as response:
                token_data = json.loads(response.read().decode())
            from google.auth.transport import requests as google_requests
            from google.oauth2 import id_token
            identity = id_token.verify_oauth2_token(token_data["id_token"], google_requests.Request(), settings.GOOGLE_CLIENT_ID)
            email = identity.get("email", "").lower().strip()
            if not email or not identity.get("email_verified"):
                raise ValueError("Google account email is not verified.")
            user, created = User.objects.get_or_create(email=email, defaults={"role": User.Role.CANDIDATE})
            if created:
                user.set_unusable_password()
                user.save(update_fields=("password",))
            refresh = RefreshToken.for_user(user)
            redirect = f"{settings.FRONTEND_URL}/auth/callback?" + urllib.parse.urlencode({"access": str(refresh.access_token), "refresh": str(refresh)})
            return HttpResponseRedirect(redirect)
        except Exception:
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/login?error=google_failed")
