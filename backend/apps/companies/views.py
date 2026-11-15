from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Company, CompanyMembership
from .permissions import IsCompanyMember
from .serializers import CompanyMembershipSerializer, CompanySerializer


class CompanyListCreateView(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(memberships__user=self.request.user).distinct().prefetch_related("memberships__user")

    def perform_create(self, serializer):
        company = serializer.save(created_by=self.request.user)
        CompanyMembership.objects.create(company=company, user=self.request.user, role=CompanyMembership.Role.OWNER)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyMember]

    def get_queryset(self):
        return Company.objects.filter(memberships__user=self.request.user).distinct().prefetch_related("memberships__user")


class CompanyMembershipView(generics.ListCreateAPIView):
    serializer_class = CompanyMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_company(self):
        return get_object_or_404(Company, pk=self.kwargs["company_id"], memberships__user=self.request.user)

    def get_queryset(self):
        return CompanyMembership.objects.filter(company=self.get_company()).select_related("user")

    def create(self, request, *args, **kwargs):
        company = self.get_company()
        if not CompanyMembership.objects.filter(company=company, user=request.user, role=CompanyMembership.Role.OWNER).exists():
            return Response({"detail": "Only company owners can manage memberships."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
