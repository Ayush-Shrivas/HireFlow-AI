from rest_framework.permissions import BasePermission
from .models import CompanyMembership


class IsCompanyMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return CompanyMembership.objects.filter(company=obj, user=request.user).exists()
