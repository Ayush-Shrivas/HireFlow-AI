from django.urls import path
from .views import InterviewDetailView, InterviewListCreateView

urlpatterns = [
    path("", InterviewListCreateView.as_view(), name="interview-list"),
    path("<int:pk>/", InterviewDetailView.as_view(), name="interview-detail"),
]
