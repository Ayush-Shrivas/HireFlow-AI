from django.db import transaction
from rest_framework.exceptions import ValidationError
from .models import Application, ApplicationStatusHistory
from apps.audit.models import AuditEvent


ALLOWED_TRANSITIONS = {
    Application.Status.APPLIED: {Application.Status.REVIEWING, Application.Status.REJECTED},
    Application.Status.REVIEWING: {Application.Status.SHORTLISTED, Application.Status.REJECTED},
    Application.Status.SHORTLISTED: {Application.Status.INTERVIEW, Application.Status.REJECTED},
    Application.Status.INTERVIEW: {Application.Status.OFFERED, Application.Status.REJECTED},
    Application.Status.OFFERED: {Application.Status.HIRED, Application.Status.REJECTED},
    Application.Status.HIRED: set(),
    Application.Status.REJECTED: set(),
}


@transaction.atomic
def transition_application(application, to_status, actor, note=""):
    if to_status not in Application.Status.values:
        raise ValidationError({"status": "Unknown application status."})
    if to_status not in ALLOWED_TRANSITIONS[application.status]:
        raise ValidationError({"status": f"Cannot transition from {application.status} to {to_status}."})
    previous = application.status
    application.status = to_status
    application.save(update_fields=("status", "updated_at"))
    ApplicationStatusHistory.objects.create(application=application, from_status=previous, to_status=to_status, changed_by=actor, note=note)
    AuditEvent.objects.create(actor=actor, action="application.status_changed", object_type="application", object_id=application.pk, metadata={"from": previous, "to": to_status})
    return application
