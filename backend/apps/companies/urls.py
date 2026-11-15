from django.urls import path
from .views import CompanyDetailView, CompanyListCreateView, CompanyMembershipView

urlpatterns = [
    path("", CompanyListCreateView.as_view()),
    path("<int:pk>/", CompanyDetailView.as_view()),
    path("<int:company_id>/members/", CompanyMembershipView.as_view()),
]
