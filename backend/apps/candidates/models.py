from django.conf import settings
from django.db import models


class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="candidate_profile")
    headline = models.CharField(max_length=160, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    years_experience = models.PositiveSmallIntegerField(default=0)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Candidate profile: {self.user.email}"


class Resume(models.Model):
    class Status(models.TextChoices):
        UPLOADED = "UPLOADED", "Uploaded"
        PROCESSING = "PROCESSING", "Processing"
        READY = "READY", "Ready"
        FAILED = "FAILED", "Failed"

    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx", "txt"}

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes")
    file = models.FileField(upload_to="resumes/%Y/%m/")
    original_filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.UPLOADED)
    extracted_text = models.TextField(blank=True)
    analysis = models.JSONField(default=dict, blank=True)
    failure_reason = models.CharField(max_length=500, blank=True)
    processing_attempts = models.PositiveSmallIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-uploaded_at",)

    def __str__(self):
        return f"Resume {self.pk} for {self.candidate.email}"
