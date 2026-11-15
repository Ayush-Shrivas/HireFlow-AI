from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.applications.models import Application
from apps.candidates.models import CandidateProfile, Resume
from apps.companies.models import Company
from apps.jobs.models import Job, JobSkill, Skill
from apps.recommendations.models import MatchResult


class MatchingTests(APITestCase):
    def setUp(self):
        self.candidate = User.objects.create_user("candidate@example.com", "StrongPassword123!", role=User.Role.CANDIDATE)
        self.recruiter = User.objects.create_user("recruiter@example.com", "StrongPassword123!", role=User.Role.RECRUITER)
        self.company = Company.objects.create(name="Acme Labs", slug="acme-labs", created_by=self.recruiter)
        CandidateProfile.objects.create(user=self.candidate, years_experience=4)
        Resume.objects.create(
            candidate=self.candidate,
            file=SimpleUploadedFile("resume.txt", b"Python Django APIs SQL"),
            original_filename="resume.txt",
            status=Resume.Status.READY,
            extracted_text="Python Django APIs SQL",
            analysis={"skills": ["Python", "Django", "SQL"]},
        )
        python = Skill.objects.create(name="Python", slug="python")
        django = Skill.objects.create(name="Django", slug="django")
        react = Skill.objects.create(name="React", slug="react")
        self.best_job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Python Django Engineer", description="Build Python APIs with Django", min_experience=2, status=Job.Status.PUBLISHED)
        self.other_job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Frontend Engineer", description="Build React interfaces", min_experience=8, status=Job.Status.PUBLISHED)
        JobSkill.objects.bulk_create([JobSkill(job=self.best_job, skill=python), JobSkill(job=self.best_job, skill=django), JobSkill(job=self.other_job, skill=react)])
        self.client.force_authenticate(self.candidate)

    def test_recommendations_are_ranked_and_explainable(self):
        response = self.client.get("/api/v1/recommendations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data["results"][0]
        self.assertEqual(result["job_id"], self.best_job.id)
        self.assertEqual(result["matched_skills"], ["django", "python"])
        self.assertEqual(result["missing_skills"], [])
        self.assertLessEqual(result["score"], 100)
        self.assertTrue(MatchResult.objects.filter(candidate=self.candidate, job=self.best_job).exists())

    def test_applied_and_closed_jobs_are_excluded(self):
        Application.objects.create(candidate=self.candidate, job=self.best_job)
        self.other_job.status = Job.Status.CLOSED
        self.other_job.save(update_fields=("status", "updated_at"))
        response = self.client.get("/api/v1/recommendations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

    def test_recruiters_cannot_view_recommendations(self):
        self.client.force_authenticate(self.recruiter)
        self.assertEqual(self.client.get("/api/v1/recommendations/").status_code, status.HTTP_403_FORBIDDEN)

