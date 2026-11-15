from rest_framework import serializers
from .models import Application, ApplicationStatusHistory


class ApplicationStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_email = serializers.EmailField(source="changed_by.email", read_only=True)

    class Meta:
        model = ApplicationStatusHistory
        fields = ("id", "from_status", "to_status", "changed_by_email", "note", "created_at")


class ApplicationSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(source="candidate.email", read_only=True)
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    history = ApplicationStatusHistorySerializer(source="status_history", many=True, read_only=True)

    class Meta:
        model = Application
        fields = ("id", "candidate", "candidate_email", "job", "job_title", "company_name", "cover_note", "status", "applied_at", "updated_at", "history")
        read_only_fields = ("id", "candidate", "candidate_email", "job_title", "company_name", "status", "applied_at", "updated_at", "history")
