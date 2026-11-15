from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.audit.models import AuditEvent
from apps.companies.models import Company, CompanyMembership
from apps.jobs.models import Job
from apps.applications.models import Application, ApplicationStatusHistory


class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.candidate = User.objects.create_user("candidate@example.com", "StrongPass123", role="CANDIDATE")
        self.recruiter = User.objects.create_user("recruiter@example.com", "StrongPass123", role="RECRUITER")
        self.outsider = User.objects.create_user("outsider@example.com", "StrongPass123", role="RECRUITER")
        self.company = Company.objects.create(name="Acme", slug="acme", created_by=self.recruiter)
        CompanyMembership.objects.create(company=self.company, user=self.recruiter, role="OWNER")
        self.job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Engineer", description="Build", status="PUBLISHED")

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_candidate_can_apply_and_duplicate_is_rejected(self):
        self.auth(self.candidate)
        first = self.client.post("/api/v1/applications/", {"job": self.job.pk, "cover_note": "Hello"}, format="json")
        duplicate = self.client.post("/api/v1/applications/", {"job": self.job.pk}, format="json")
        self.assertEqual(first.status_code, 201)
        self.assertEqual(duplicate.status_code, 400)
        self.assertEqual(AuditEvent.objects.filter(action="application.created").count(), 1)

    def test_recruiter_can_transition_and_invalid_transition_is_rejected(self):
        application = Application.objects.create(candidate=self.candidate, job=self.job)
        self.auth(self.recruiter)
        ok = self.client.post(f"/api/v1/applications/{application.pk}/transition/", {"status": "REVIEWING"}, format="json")
        bad = self.client.post(f"/api/v1/applications/{application.pk}/transition/", {"status": "HIRED"}, format="json")
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(bad.status_code, 400)
        self.assertEqual(ApplicationStatusHistory.objects.count(), 1)

    def test_role_isolation(self):
        application = Application.objects.create(candidate=self.candidate, job=self.job)
        self.auth(self.outsider)
        self.assertEqual(self.client.get(f"/api/v1/applications/{application.pk}/").status_code, 404)
        self.assertEqual(self.client.post(f"/api/v1/applications/{application.pk}/transition/", {"status": "REVIEWING"}, format="json").status_code, 403)
