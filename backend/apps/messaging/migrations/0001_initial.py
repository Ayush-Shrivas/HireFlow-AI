from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Conversation", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("participants", models.ManyToManyField(related_name="conversations", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Message", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("body", models.TextField(max_length=5000)), ("read_at", models.DateTimeField(blank=True, null=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("conversation", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="messaging.conversation")),
            ("sender", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sent_messages", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ("created_at",)}),
    ]
