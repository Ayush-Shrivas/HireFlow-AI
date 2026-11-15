from django.db.models import Count
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.applications.models import Application
from apps.interviews.models import Interview
from apps.jobs.models import Job


class DashboardMetricsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role == User.Role.CANDIDATE:
            applications = Application.objects.filter(candidate=request.user)
            return Response({
                "role": "CANDIDATE",
                "published_jobs": Job.objects.filter(status=Job.Status.PUBLISHED).count(),
                "applications": applications.count(),
                "interviews": Interview.objects.filter(application__candidate=request.user, status=Interview.Status.SCHEDULED).count(),
                "unread_messages": request.user.conversations.filter(messages__read_at__isnull=True).exclude(messages__sender=request.user).distinct().count(),
            })
        if request.user.role == User.Role.RECRUITER:
            company_ids = request.user.company_memberships.values_list("company_id", flat=True)
            jobs = Job.objects.filter(company_id__in=company_ids)
            return Response({
                "role": "RECRUITER",
                "published_jobs": jobs.filter(status=Job.Status.PUBLISHED).count(),
                "applications": Application.objects.filter(job__company_id__in=company_ids).count(),
                "interviews": Interview.objects.filter(application__job__company_id__in=company_ids, status=Interview.Status.SCHEDULED).count(),
                "unread_messages": request.user.conversations.filter(messages__read_at__isnull=True).exclude(messages__sender=request.user).distinct().count(),
            })
        raise PermissionDenied("Dashboard metrics are not available for this account.")
