from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import CustomUser


class RegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_can_register(self):
        data = {
            "email": "test@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        self.assertTrue(CustomUser.objects.filter(email="test@example.com").exists())

        user = CustomUser.objects.get(email="test@example.com")
        self.assertEqual(user.username, "test@example.com")
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_register_password_mismatch(self):
        data = {
            "email": "test2@example.com",
            "password1": "Password123!",
            "password2": "DifferentPassword!",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(CustomUser.objects.filter(email="test2@example.com").exists())

    def test_register_duplicate_email(self):
        CustomUser.objects.create_user(
            email="test@example.com", password="Password123!"
        )

        data = {
            "email": "test@example.com",
            "password1": "Password123!",
            "password2": "Password123!",
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.filter(email="test@example.com").count(), 1)
