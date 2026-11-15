from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("candidates", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Resume", options={"ordering": ("-uploaded_at",)}, fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("file", models.FileField(upload_to="resumes/%Y/%m/")),
        ("original_filename", models.CharField(max_length=255)),
        ("content_type", models.CharField(blank=True, max_length=120)),
        ("status", models.CharField(choices=[("UPLOADED", "Uploaded"), ("PROCESSING", "Processing"), ("READY", "Ready"), ("FAILED", "Failed")], default="UPLOADED", max_length=20)),
        ("extracted_text", models.TextField(blank=True)),
        ("analysis", models.JSONField(blank=True, default=dict)),
        ("failure_reason", models.CharField(blank=True, max_length=500)),
        ("processing_attempts", models.PositiveSmallIntegerField(default=0)),
        ("uploaded_at", models.DateTimeField(auto_now_add=True)),
        ("processed_at", models.DateTimeField(blank=True, null=True)),
        ("updated_at", models.DateTimeField(auto_now=True)),
        ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resumes", to=settings.AUTH_USER_MODEL)),
    ])]
