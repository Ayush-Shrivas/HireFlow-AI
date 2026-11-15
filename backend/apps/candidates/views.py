from rest_framework import generics, permissions
from apps.accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from .models import CandidateProfile, Resume
from .serializers import CandidateProfileSerializer, ResumeSerializer
from .tasks import process_resume


class CandidateProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        if self.request.user.role != User.Role.CANDIDATE:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only candidate accounts can manage candidate profiles.")
        profile, _ = CandidateProfile.objects.get_or_create(user=self.request.user)
        return profile

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.Role.CANDIDATE:
            return Resume.objects.none()
        return Resume.objects.filter(candidate=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.role != User.Role.CANDIDATE:
            return Response({"detail": "Only candidates can upload resumes."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save(candidate=request.user, original_filename=request.data["file"].name, content_type=request.data["file"].content_type or "")
        process_resume.delay(resume.pk)
        return Response(self.get_serializer(resume).data, status=status.HTTP_201_CREATED)


class ResumeDetailView(generics.RetrieveAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.Role.CANDIDATE:
            return Resume.objects.none()
        return Resume.objects.filter(candidate=self.request.user)
