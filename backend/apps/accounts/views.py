import json
import secrets
import urllib.parse
import urllib.request

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


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
