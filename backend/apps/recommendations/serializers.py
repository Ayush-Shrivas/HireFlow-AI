from rest_framework import serializers
from .models import MatchResult


class MatchResultSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    job_id = serializers.IntegerField(source="job.id", read_only=True)

    class Meta:
        model = MatchResult
        fields = ("id", "job_id", "job_title", "company_name", "score", "skill_score", "experience_score", "semantic_score", "matched_skills", "missing_skills", "explanation", "calculated_at")
        read_only_fields = fields
