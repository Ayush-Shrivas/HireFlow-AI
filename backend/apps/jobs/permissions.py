from rest_framework.permissions import BasePermission
from apps.companies.models import CompanyMembership


class IsJobCompanyMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return CompanyMembership.objects.filter(company=obj.company, user=request.user).exists()
