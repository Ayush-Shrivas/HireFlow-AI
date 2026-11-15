from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("applications", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Interview", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("start_at", models.DateTimeField()), ("end_at", models.DateTimeField()),
        ("meeting_url", models.URLField(blank=True)),
        ("status", models.CharField(choices=[("SCHEDULED", "Scheduled"), ("COMPLETED", "Completed"), ("CANCELLED", "Cancelled")], default="SCHEDULED", max_length=20)),
        ("notes", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ("application", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="interviews", to="applications.application")),
        ("scheduled_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="scheduled_interviews", to=settings.AUTH_USER_MODEL)),
    ], options={"ordering": ("start_at",)})]
