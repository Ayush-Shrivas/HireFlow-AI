from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("jobs", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(
        name="MatchResult",
        fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("score", models.PositiveSmallIntegerField()),
            ("skill_score", models.PositiveSmallIntegerField()),
            ("experience_score", models.PositiveSmallIntegerField()),
            ("semantic_score", models.PositiveSmallIntegerField()),
            ("matched_skills", models.JSONField(default=list)),
            ("missing_skills", models.JSONField(default=list)),
            ("explanation", models.JSONField(default=dict)),
            ("calculated_at", models.DateTimeField(auto_now=True)),
            ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="match_results", to=settings.AUTH_USER_MODEL)),
            ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="match_results", to="jobs.job")),
        ],
        options={"ordering": ("-score", "job__id")},
    ), migrations.AddConstraint(
        model_name="matchresult",
        constraint=models.UniqueConstraint(fields=("candidate", "job"), name="unique_candidate_job_match"),
    )]
