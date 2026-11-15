from rest_framework import serializers
from .models import RecruiterProfile


class RecruiterProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = RecruiterProfile
        fields = ("id", "email", "full_name", "job_title", "bio", "created_at", "updated_at")
        read_only_fields = ("id", "email", "created_at", "updated_at")
