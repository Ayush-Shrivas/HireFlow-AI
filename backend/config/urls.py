from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse
from django.db import connection


def health(request):
    return JsonResponse({"status": "ok", "service": "backend"})


def readiness(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "ready", "checks": {"database": "ok"}})
    except Exception:
        return JsonResponse({"status": "not_ready", "checks": {"database": "failed"}}, status=503)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("health/ready/", readiness),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/candidates/", include("apps.candidates.urls")),
    path("api/v1/recruiters/", include("apps.recruiters.urls")),
    path("api/v1/companies/", include("apps.companies.urls")),
    path("api/v1/jobs/", include("apps.jobs.urls")),
    path("api/v1/applications/", include("apps.applications.urls")),
    path("api/v1/resumes/", include("apps.candidates.resume_urls")),
    path("api/v1/recommendations/", include("apps.recommendations.urls")),
    path("api/v1/interviews/", include("apps.interviews.urls")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/conversations/", include("apps.messaging.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
]
