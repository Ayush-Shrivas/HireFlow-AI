from django.conf import settings
from django.db import models
from apps.applications.models import Application


class Interview(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        COMPLETED = "COMPLETED", "Completed"
        CANCELLED = "CANCELLED", "Cancelled"

    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="interviews")
    scheduled_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="scheduled_interviews")
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    meeting_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SCHEDULED)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("start_at",)
