from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.accounts.models import User
from apps.applications.models import Application
from apps.companies.models import CompanyMembership
from apps.notifications.services import create_notification
from .models import Interview
from .serializers import InterviewSerializer


def visible_interviews(user):
    if user.role == User.Role.CANDIDATE:
        return Interview.objects.filter(application__candidate=user)
    if user.role == User.Role.RECRUITER:
        return Interview.objects.filter(application__job__company__memberships__user=user)
    return Interview.objects.all()


class InterviewListCreateView(generics.ListCreateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return visible_interviews(self.request.user).select_related("application__candidate", "application__job__company")

    def perform_create(self, serializer):
        if self.request.user.role not in (User.Role.RECRUITER, User.Role.ADMIN):
            raise PermissionDenied("Only recruiters can schedule interviews.")
        application = get_object_or_404(Application.objects.select_related("job__company", "candidate"), pk=serializer.validated_data["application"].pk)
        if self.request.user.role != User.Role.ADMIN and not CompanyMembership.objects.filter(company=application.job.company, user=self.request.user).exists():
            raise PermissionDenied("You cannot schedule an interview for this company.")
        interview = serializer.save(scheduled_by=self.request.user)
        create_notification(application.candidate, "INTERVIEW_SCHEDULED", "Interview scheduled", f"An interview was scheduled for {application.job.title}.")


class InterviewDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = InterviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return visible_interviews(self.request.user).select_related("application__candidate", "application__job__company")

