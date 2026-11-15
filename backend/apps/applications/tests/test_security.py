from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.companies.models import Company, CompanyMembership
from apps.jobs.models import Job
from apps.applications.models import Application


class ApplicationSecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.candidate = User.objects.create_user("candidate-security@example.com", "StrongPass123!", role="CANDIDATE")
        self.other_candidate = User.objects.create_user("other-candidate@example.com", "StrongPass123!", role="CANDIDATE")
        self.recruiter = User.objects.create_user("recruiter-security@example.com", "StrongPass123!", role="RECRUITER")
        self.outsider = User.objects.create_user("outsider-security@example.com", "StrongPass123!", role="RECRUITER")
        self.company = Company.objects.create(name="Security Co", slug="security-co", created_by=self.recruiter)
        CompanyMembership.objects.create(company=self.company, user=self.recruiter, role="OWNER")
        self.job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Security Engineer", status=Job.Status.PUBLISHED)
        self.application = Application.objects.create(candidate=self.candidate, job=self.job)

    def test_candidate_cannot_read_another_candidate_application(self):
        self.client.force_authenticate(user=self.other_candidate)
        response = self.client.get(f"/api/v1/applications/{self.application.pk}/")
        self.assertEqual(response.status_code, 404)

    def test_non_member_cannot_transition_or_close_company_data(self):
        self.client.force_authenticate(user=self.outsider)
        transition = self.client.post(f"/api/v1/applications/{self.application.pk}/transition/", {"status": "REVIEWING"}, format="json")
        close = self.client.post(f"/api/v1/jobs/{self.job.pk}/close/")
        self.assertEqual(transition.status_code, 403)
        self.assertEqual(close.status_code, 404)
