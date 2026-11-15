try:
    from celery import shared_task
except ModuleNotFoundError:
    class _LocalTask:
        def __init__(self, function, bind=False):
            self.function = function
            self.bind = bind

        def __call__(self, *args, **kwargs):
            return self.function(None, *args, **kwargs) if self.bind else self.function(*args, **kwargs)

        def delay(self, *args, **kwargs):
            return self(*args, **kwargs)

    def shared_task(*, bind=False, **_options):
        def decorator(function):
            return _LocalTask(function, bind=bind)
        return decorator

from django.utils import timezone as django_timezone

from .models import Resume
from .resume_services import analyze_with_ai, extract_resume_text


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def process_resume(self, resume_id):
    try:
        resume = Resume.objects.get(pk=resume_id)
        resume.status = Resume.Status.PROCESSING
        resume.processing_attempts += 1
        resume.failure_reason = ""
        resume.save(update_fields=("status", "processing_attempts", "failure_reason", "updated_at"))
        text = extract_resume_text(resume)
        if not text:
            raise ValueError("The document contains no extractable text.")
        resume.extracted_text = text
        resume.analysis = analyze_with_ai(text, resume.original_filename)
        resume.status = Resume.Status.READY
        resume.processed_at = django_timezone.now()
        resume.save(update_fields=("extracted_text", "analysis", "status", "processed_at", "updated_at"))
        return {"resume_id": resume.pk, "status": resume.status}
    except Resume.DoesNotExist:
        return {"resume_id": resume_id, "status": "missing"}
    except Exception as exc:
        resume = Resume.objects.get(pk=resume_id)
        resume.status = Resume.Status.FAILED
        resume.failure_reason = str(exc)[:500]
        resume.save(update_fields=("status", "failure_reason", "updated_at"))
        if self is not None and hasattr(self, "retry"):
            raise self.retry(exc=exc)
        return {"resume_id": resume_id, "status": resume.status}
