from django.conf import settings
from django.db import models


class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recruiter_profile")
    full_name = models.CharField(max_length=160, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recruiter profile: {self.user.email}"
