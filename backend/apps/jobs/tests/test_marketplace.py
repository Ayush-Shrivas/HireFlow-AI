from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User
from apps.companies.models import Company, CompanyMembership
from apps.jobs.models import Job, Skill


class DayTwoMarketplaceTests(APITestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user("recruiter@example.com", "StrongPassword123!", role=User.Role.RECRUITER)
        self.other_recruiter = User.objects.create_user("other@example.com", "StrongPassword123!", role=User.Role.RECRUITER)
        self.candidate = User.objects.create_user("candidate@example.com", "StrongPassword123!", role=User.Role.CANDIDATE)
        self.company = Company.objects.create(name="Acme Labs", slug="acme-labs", created_by=self.recruiter)
        CompanyMembership.objects.create(company=self.company, user=self.recruiter, role=CompanyMembership.Role.OWNER)

    def auth(self, user):
        self.client.force_authenticate(user=user)

    def test_candidate_can_create_and_update_own_profile(self):
        self.auth(self.candidate)
        response = self.client.patch("/api/v1/candidates/profile/", {"headline": "Frontend engineer", "years_experience": 4}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["headline"], "Frontend engineer")

    def test_company_creation_creates_owner_membership(self):
        self.auth(self.recruiter)
        response = self.client.post("/api/v1/companies/", {"name": "New Co", "description": "A new company"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CompanyMembership.objects.filter(company_id=response.data["id"], user=self.recruiter, role="OWNER").exists())

    def test_only_members_can_create_and_publish_jobs(self):
        skill = Skill.objects.create(name="Django", slug="django")
        self.auth(self.other_recruiter)
        forbidden = self.client.post("/api/v1/jobs/", {"company": self.company.id, "title": "Engineer", "description": "Build things"}, format="json")
        self.assertEqual(forbidden.status_code, status.HTTP_403_FORBIDDEN)
        self.auth(self.recruiter)
        created = self.client.post("/api/v1/jobs/", {"company": self.company.id, "title": "Engineer", "description": "Build things", "skill_ids": [skill.id]}, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        published = self.client.post(f"/api/v1/jobs/{created.data['id']}/publish/")
        self.assertEqual(published.status_code, status.HTTP_200_OK)
        self.assertEqual(published.data["status"], "PUBLISHED")

    def test_public_job_search_and_pagination(self):
        job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Senior Python Engineer", description="Python and APIs", status=Job.Status.PUBLISHED)
        self.auth(self.candidate)
        response = self.client.get("/api/v1/jobs/?search=Python&page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], job.id)

    def test_non_member_cannot_update_company(self):
        self.auth(self.other_recruiter)
        response = self.client.patch(f"/api/v1/companies/{self.company.id}/", {"description": "changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
