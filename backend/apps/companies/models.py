from django.conf import settings
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=160, unique=True)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_companies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CompanyMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        RECRUITER = "RECRUITER", "Recruiter"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company_memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RECRUITER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("company", "user"), name="unique_company_member")]
