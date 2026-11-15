from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.audit.models import AuditEvent
from apps.jobs.models import Job
from apps.companies.models import CompanyMembership
from .models import Application
from .serializers import ApplicationSerializer
from .services import transition_application


def visible_applications(user):
    if user.role == "CANDIDATE":
        return Application.objects.filter(candidate=user)
    if user.role == "RECRUITER":
        return Application.objects.filter(job__company__memberships__user=user)
    return Application.objects.all()


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return visible_applications(self.request.user).select_related("candidate", "job", "job__company").prefetch_related("status_history__changed_by")

    def create(self, request, *args, **kwargs):
        if request.user.role != "CANDIDATE":
            return Response({"detail": "Only candidates can submit applications."}, status=status.HTTP_403_FORBIDDEN)
        job = get_object_or_404(Job, pk=request.data.get("job"), status=Job.Status.PUBLISHED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                application = serializer.save(candidate=request.user, job=job)
        except IntegrityError:
            return Response({"detail": "You have already applied to this job."}, status=status.HTTP_400_BAD_REQUEST)
        AuditEvent.objects.create(actor=request.user, action="application.created", object_type="application", object_id=application.pk, metadata={"job_id": job.pk})
        return Response(self.get_serializer(application).data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(generics.RetrieveAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return visible_applications(self.request.user).select_related("candidate", "job", "job__company").prefetch_related("status_history__changed_by")


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def transition_view(request, pk):
    application = get_object_or_404(Application.objects.select_related("job__company"), pk=pk)
    if request.user.role != "ADMIN" and not CompanyMembership.objects.filter(company=application.job.company, user=request.user).exists():
        return Response({"detail": "Only recruiters in this company can update the application."}, status=status.HTTP_403_FORBIDDEN)
    application = transition_application(application, request.data.get("status"), request.user, request.data.get("note", ""))
    return Response(ApplicationSerializer(application).data)
