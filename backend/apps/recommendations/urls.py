from django.urls import path
from .views import RecommendationDetailView, RecommendationListView

urlpatterns = [
    path("", RecommendationListView.as_view(), name="recommendation-list"),
    path("<int:job_id>/", RecommendationDetailView.as_view(), name="recommendation-detail"),
]
