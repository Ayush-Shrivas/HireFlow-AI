from pathlib import Path
from django.conf import settings
from rest_framework import serializers
from .models import CandidateProfile, Resume


class CandidateProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = CandidateProfile
        fields = ("id", "email", "headline", "bio", "location", "years_experience", "portfolio_url", "created_at", "updated_at")
        read_only_fields = ("id", "email", "created_at", "updated_at")


class ResumeSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ("id", "file", "file_url", "original_filename", "content_type", "status", "extracted_text", "analysis", "failure_reason", "processing_attempts", "uploaded_at", "processed_at", "updated_at")
        read_only_fields = ("id", "file_url", "original_filename", "content_type", "status", "extracted_text", "analysis", "failure_reason", "processing_attempts", "uploaded_at", "processed_at", "updated_at")

    def validate_file(self, value):
        if value.size == 0:
            raise serializers.ValidationError("The resume file cannot be empty.")
        if value.size > settings.RESUME_MAX_SIZE_BYTES:
            raise serializers.ValidationError(f"Resume files must be {settings.RESUME_MAX_SIZE_BYTES // (1024 * 1024)} MB or smaller.")
        extension = Path(value.name).suffix.lower().lstrip(".")
        if extension not in Resume.ALLOWED_EXTENSIONS:
            raise serializers.ValidationError("Only PDF, DOC, DOCX, and TXT resumes are supported.")
        if value.content_type and value.content_type == "application/x-msdownload":
            raise serializers.ValidationError("Executable files are not allowed.")
        return value

    def get_file_url(self, obj):
        request = self.context.get("request")
        if not request:
            return None
        return request.build_absolute_uri(obj.file.url)
