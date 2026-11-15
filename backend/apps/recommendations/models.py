from django.conf import settings
from django.db import models
from apps.jobs.models import Job


class MatchResult(models.Model):
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="match_results")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="match_results")
    score = models.PositiveSmallIntegerField()
    skill_score = models.PositiveSmallIntegerField()
    experience_score = models.PositiveSmallIntegerField()
    semantic_score = models.PositiveSmallIntegerField()
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    explanation = models.JSONField(default=dict)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-score", "job__id")
        constraints = [models.UniqueConstraint(fields=("candidate", "job"), name="unique_candidate_job_match")]

