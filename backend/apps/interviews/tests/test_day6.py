from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.applications.models import Application
from apps.companies.models import Company, CompanyMembership
from apps.jobs.models import Job
from apps.messaging.models import Message
from apps.notifications.models import Notification


class DaySixWorkflowTests(APITestCase):
    def setUp(self):
        self.candidate = User.objects.create_user("candidate@example.com", "StrongPassword123!", role=User.Role.CANDIDATE)
        self.recruiter = User.objects.create_user("recruiter@example.com", "StrongPassword123!", role=User.Role.RECRUITER)
        self.other = User.objects.create_user("other@example.com", "StrongPassword123!", role=User.Role.CANDIDATE)
        self.company = Company.objects.create(name="Acme Labs", slug="acme-labs", created_by=self.recruiter)
        CompanyMembership.objects.create(company=self.company, user=self.recruiter, role=CompanyMembership.Role.OWNER)
        self.job = Job.objects.create(company=self.company, created_by=self.recruiter, title="Engineer", description="Build APIs", status=Job.Status.PUBLISHED)
        self.application = Application.objects.create(candidate=self.candidate, job=self.job)

    def auth(self, user):
        self.client.force_authenticate(user)

    def test_recruiter_schedules_interview_and_candidate_receives_notification(self):
        self.auth(self.recruiter)
        start = timezone.now() + timedelta(days=1)
        response = self.client.post("/api/v1/interviews/", {"application": self.application.id, "start_at": start.isoformat(), "end_at": (start + timedelta(hours=1)).isoformat(), "meeting_url": "https://meet.example.com/abc"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.auth(self.candidate)
        notifications = self.client.get("/api/v1/notifications/")
        self.assertEqual(notifications.status_code, status.HTTP_200_OK)
        self.assertEqual(notifications.data["results"][0]["notification_type"], "INTERVIEW_SCHEDULED")

    def test_interview_access_is_scoped(self):
        self.auth(self.recruiter)
        start = timezone.now() + timedelta(days=1)
        interview = self.client.post("/api/v1/interviews/", {"application": self.application.id, "start_at": start.isoformat(), "end_at": (start + timedelta(hours=1)).isoformat()}, format="json")
        self.auth(self.other)
        self.assertEqual(self.client.get(f"/api/v1/interviews/{interview.data['id']}/").status_code, status.HTTP_404_NOT_FOUND)

    def test_messages_create_notifications_and_read_state(self):
        self.auth(self.candidate)
        conversation = self.client.post("/api/v1/conversations/", {"participant_ids": [self.candidate.id, self.recruiter.id]}, format="json")
        self.assertEqual(conversation.status_code, status.HTTP_201_CREATED)
        conversation_id = conversation.data["id"]
        message = self.client.post(f"/api/v1/conversations/{conversation_id}/messages/", {"body": "Hello recruiter"}, format="json")
        self.assertEqual(message.status_code, status.HTTP_201_CREATED)
        self.auth(self.recruiter)
        self.assertEqual(Notification.objects.filter(recipient=self.recruiter, notification_type="MESSAGE_RECEIVED").count(), 1)
        self.assertEqual(self.client.get(f"/api/v1/conversations/{conversation_id}/messages/").status_code, status.HTTP_200_OK)
        read = self.client.patch(f"/api/v1/conversations/messages/{message.data['id']}/read/", {}, format="json")
        self.assertEqual(read.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(Message.objects.get(pk=message.data["id"]).read_at)

    def test_dashboard_metrics_are_role_scoped(self):
        self.auth(self.candidate)
        candidate_metrics = self.client.get("/api/v1/analytics/dashboard/")
        self.assertEqual(candidate_metrics.status_code, status.HTTP_200_OK)
        self.assertEqual(candidate_metrics.data["applications"], 1)
        self.auth(self.recruiter)
        recruiter_metrics = self.client.get("/api/v1/analytics/dashboard/")
        self.assertEqual(recruiter_metrics.status_code, status.HTTP_200_OK)
        self.assertEqual(recruiter_metrics.data["published_jobs"], 1)
