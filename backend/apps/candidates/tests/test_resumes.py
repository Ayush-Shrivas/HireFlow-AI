import tempfile
from unittest.mock import patch

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.accounts.models import User
from apps.candidates.models import Resume
from apps.candidates.tasks import process_resume


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ResumeWorkflowTests(APITestCase):
    def setUp(self):
        self.candidate = User.objects.create_user("candidate@example.com", "StrongPass123!", role=User.Role.CANDIDATE)
        self.recruiter = User.objects.create_user("recruiter@example.com", "StrongPass123!", role=User.Role.RECRUITER)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.candidate).access_token}")

    def upload(self, name="resume.txt", content=b"Python Django SQL experience"):
        return self.client.post(reverse("resume-list"), {"file": SimpleUploadedFile(name, content, content_type="text/plain")}, format="multipart")

    def test_candidate_uploads_and_processes_text_resume(self):
        response = self.upload()
        self.assertEqual(response.status_code, 201)
        resume = Resume.objects.get()
        self.assertEqual(resume.status, Resume.Status.READY)
        self.assertEqual(resume.extracted_text, "Python Django SQL experience")

    def test_rejects_empty_unsafe_and_oversized_files(self):
        self.assertEqual(self.upload(content=b"").status_code, 400)
        self.assertEqual(self.upload(name="resume.exe").status_code, 400)
        with self.settings(RESUME_MAX_SIZE_BYTES=3):
            self.assertEqual(self.upload(content=b"more than three bytes").status_code, 400)

    def test_recruiter_cannot_upload_or_view_candidate_resume(self):
        response = self.upload()
        resume_id = response.data["id"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.recruiter).access_token}")
        self.assertEqual(self.upload().status_code, 403)
        self.assertEqual(self.client.get(reverse("resume-detail", args=[resume_id])).status_code, 404)

    @patch("apps.candidates.tasks.analyze_with_ai", return_value={"skills": ["python"]})
    def test_processing_failure_is_recorded(self, _analyze):
        resume = Resume.objects.create(candidate=self.candidate, file=SimpleUploadedFile("empty.txt", b""), original_filename="empty.txt", content_type="text/plain")
        result = process_resume.delay(resume.pk)
        resume.refresh_from_db()
        self.assertEqual(result["status"], Resume.Status.FAILED)
        self.assertEqual(resume.status, Resume.Status.FAILED)
        self.assertIn("extractable text", resume.failure_reason)
