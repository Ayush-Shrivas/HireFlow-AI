from rest_framework import generics, permissions
from apps.accounts.models import User
from .models import RecruiterProfile
from .serializers import RecruiterProfileSerializer


class RecruiterProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = RecruiterProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != User.Role.RECRUITER:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only recruiter accounts can manage recruiter profiles.")
        profile, _ = RecruiterProfile.objects.get_or_create(user=self.request.user)
        return profile
