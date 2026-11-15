from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("jobs", "0001_initial"), ("audit", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cover_note", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("APPLIED", "Applied"), ("REVIEWING", "Reviewing"), ("SHORTLISTED", "Shortlisted"), ("INTERVIEW", "Interview"), ("OFFERED", "Offered"), ("HIRED", "Hired"), ("REJECTED", "Rejected")], default="APPLIED", max_length=20)),
                ("applied_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to=settings.AUTH_USER_MODEL)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="jobs.job")),
            ],
            options={"ordering": ("-applied_at",)},
        ),
        migrations.CreateModel(
            name="ApplicationStatusHistory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("from_status", models.CharField(blank=True, max_length=20)),
                ("to_status", models.CharField(max_length=20)),
                ("note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("application", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="status_history", to="applications.application")),
                ("changed_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="application_status_changes", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ("created_at",)},
        ),
        migrations.AddConstraint(model_name="application", constraint=models.UniqueConstraint(fields=("candidate", "job"), name="unique_candidate_job_application")),
    ]
