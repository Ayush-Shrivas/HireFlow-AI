from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.companies.models import CompanyMembership
from .models import Job, Skill
from .permissions import IsJobCompanyMember
from .serializers import JobSerializer, SkillSerializer


class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ("name",)
    filter_backends = (SearchFilter,)


class JobViewSet(ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title", "description", "location", "company__name", "skills__name")
    ordering_fields = ("created_at", "title", "min_experience", "salary_min")
    ordering = ("-created_at",)

    def get_queryset(self):
        queryset = Job.objects.select_related("company", "created_by").prefetch_related("skills")
        if self.request.query_params.get("location"):
            queryset = queryset.filter(location__icontains=self.request.query_params["location"])
        if self.request.query_params.get("employment_type"):
            queryset = queryset.filter(employment_type=self.request.query_params["employment_type"])
        if self.request.query_params.get("min_experience"):
            queryset = queryset.filter(min_experience__lte=self.request.query_params["min_experience"])
        if self.request.user.role == "ADMIN":
            return queryset
        owned = Q(company__memberships__user=self.request.user)
        if self.action in ("list", "retrieve"):
            return queryset.filter(Q(status=Job.Status.PUBLISHED) | owned).distinct()
        return queryset.filter(owned).distinct()

    def perform_create(self, serializer):
        company = serializer.validated_data["company"]
        if not CompanyMembership.objects.filter(company=company, user=self.request.user).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must be a company member to create jobs.")
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        job = self.get_object()
        if job.status == Job.Status.CLOSED:
            return Response({"detail": "Closed jobs cannot be published."}, status=status.HTTP_400_BAD_REQUEST)
        job.status = Job.Status.PUBLISHED
        job.published_at = timezone.now()
        job.save(update_fields=("status", "published_at", "updated_at"))
        return Response(self.get_serializer(job).data)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        job = self.get_object()
        job.status = Job.Status.CLOSED
        job.save(update_fields=("status", "updated_at"))
        return Response(self.get_serializer(job).data)
