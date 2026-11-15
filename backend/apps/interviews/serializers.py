from rest_framework import serializers
from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    candidate_email = serializers.EmailField(source="application.candidate.email", read_only=True)
    job_title = serializers.CharField(source="application.job.title", read_only=True)
    company_name = serializers.CharField(source="application.job.company.name", read_only=True)

    class Meta:
        model = Interview
        fields = ("id", "application", "candidate_email", "job_title", "company_name", "start_at", "end_at", "meeting_url", "status", "notes", "scheduled_by", "created_at", "updated_at")
        read_only_fields = ("id", "candidate_email", "job_title", "company_name", "scheduled_by", "created_at", "updated_at")

    def validate(self, attrs):
        if attrs.get("end_at") and attrs.get("start_at") and attrs["end_at"] <= attrs["start_at"]:
            raise serializers.ValidationError({"end_at": "The interview must end after it starts."})
        return attrs
