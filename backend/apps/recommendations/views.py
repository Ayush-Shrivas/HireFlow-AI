from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from apps.accounts.models import User
from apps.jobs.models import Job
from .models import MatchResult
from .serializers import MatchResultSerializer
from .services import create_or_update_match, recommendation_queryset


class RecommendationListView(generics.ListAPIView):
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.Role.CANDIDATE:
            raise PermissionDenied("Only candidates can view recommendations.")
        results = [create_or_update_match(self.request.user, job) for job in recommendation_queryset(self.request.user)]
        return MatchResult.objects.filter(id__in=[result.id for result in results]).select_related("job", "job__company").order_by("-score", "job_id")


class RecommendationDetailView(generics.RetrieveAPIView):
    serializer_class = MatchResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != User.Role.CANDIDATE:
            raise PermissionDenied("Only candidates can view recommendations.")
        job = get_object_or_404(Job, pk=self.kwargs["job_id"], status=Job.Status.PUBLISHED)
        if self.request.user.applications.filter(job=job).exists():
            from rest_framework.exceptions import NotFound
            raise NotFound("Recommendations are not available for jobs you have already applied to.")
        return create_or_update_match(self.request.user, job)
