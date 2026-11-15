from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, SkillViewSet

router = DefaultRouter()
router.register("skills", SkillViewSet, basename="skill")
router.register("", JobViewSet, basename="job")

urlpatterns = [path("", include(router.urls))]
