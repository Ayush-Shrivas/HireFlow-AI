from django.urls import path
from .views import ApplicationDetailView, ApplicationListCreateView, transition_view

urlpatterns = [
    path("", ApplicationListCreateView.as_view()),
    path("<int:pk>/", ApplicationDetailView.as_view()),
    path("<int:pk>/transition/", transition_view),
]
