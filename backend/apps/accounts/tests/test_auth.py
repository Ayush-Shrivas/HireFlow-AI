from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.accounts.models import User


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_candidate_registration(self):
        response = self.client.post("/api/v1/auth/register/", {"email": "candidate@example.com", "password": "StrongPass123!", "password_confirmation": "StrongPass123!", "role": "CANDIDATE"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="candidate@example.com", role=User.Role.CANDIDATE).exists())

    def test_public_admin_registration_is_rejected(self):
        response = self.client.post("/api/v1/auth/register/", {"email": "admin@example.com", "password": "StrongPass123!", "password_confirmation": "StrongPass123!", "role": "ADMIN"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_login_me_and_logout(self):
        User.objects.create_user(email="user@example.com", password="StrongPass123!", role=User.Role.CANDIDATE)
        login = self.client.post("/api/v1/auth/login/", {"email": "user@example.com", "password": "StrongPass123!"}, format="json")
        self.assertEqual(login.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 200)
        logout = self.client.post("/api/v1/auth/logout/", {"refresh": login.data["refresh"]}, format="json")
        self.assertEqual(logout.status_code, 204)

    def test_me_requires_authentication(self):
        self.assertEqual(self.client.get("/api/v1/auth/me/").status_code, 401)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(email="duplicate@example.com", password="StrongPass123!")
        response = self.client.post("/api/v1/auth/register/", {"email": "duplicate@example.com", "password": "StrongPass123!", "password_confirmation": "StrongPass123!", "role": "CANDIDATE"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_password_confirmation_is_required_to_match(self):
        response = self.client.post("/api/v1/auth/register/", {"email": "mismatch@example.com", "password": "StrongPass123!", "password_confirmation": "DifferentPass123!", "role": "CANDIDATE"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_google_sign_in_requires_configuration(self):
        response = self.client.get("/api/v1/auth/google/login/")
        self.assertEqual(response.status_code, 503)

    @override_settings(DEBUG=True)
    def test_password_reset_request_and_confirmation(self):
        user = User.objects.create_user(email="reset@example.com", password="OldPass123!", role=User.Role.CANDIDATE)
        request = self.client.post("/api/v1/auth/password-reset/", {"email": user.email}, format="json")
        self.assertEqual(request.status_code, 200)
        self.assertIn("uid", request.data)
        confirm = self.client.post("/api/v1/auth/password-reset/confirm/", {"uid": request.data["uid"], "token": request.data["token"], "password": "NewPass123!", "password_confirmation": "NewPass123!"}, format="json")
        self.assertEqual(confirm.status_code, 200)
        self.assertEqual(self.client.post("/api/v1/auth/login/", {"email": user.email, "password": "NewPass123!"}, format="json").status_code, 200)
