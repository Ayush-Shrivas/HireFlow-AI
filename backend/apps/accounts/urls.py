from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import GoogleCallbackView, GoogleLoginView, LoginView, LogoutView, MeView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", MeView.as_view()),
    path("google/login/", GoogleLoginView.as_view()),
    path("google/callback/", GoogleCallbackView.as_view()),
]
