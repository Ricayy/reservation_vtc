from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import CustomUser


class LoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse("login")

        self.email = "login@test.com"
        self.password = "StrongPassword123!"

        self.user = CustomUser.objects.create_user(
            username=self.email, email=self.email, password=self.password
        )

    def test_login_page_loads(self):
        """La page de login répond en 200 et utilise le bon template"""
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_user_can_login_with_valid_credentials(self):
        """Un utilisateur peut se connecter avec de bons identifiants"""
        data = {"email": self.email, "password": self.password}

        response = self.client.post(self.url, data)

        # Redirection après connexion
        self.assertEqual(response.status_code, 302)

        # Vérifie que l'utilisateur est authentifié
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.email, self.email)

    def test_login_fails_with_wrong_password(self):
        """La connexion échoue si le mot de passe est incorrect"""
        data = {"email": self.email, "password": "WrongPassword!"}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertContains(response, "Email ou mot de passe incorrect")

    def test_login_fails_with_unknown_user(self):
        """La connexion échoue si l'utilisateur n'existe pas"""
        data = {"email": "unknown@test.com", "password": "SomePassword123!"}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        self.assertContains(response, "Email ou mot de passe incorrect")

    def test_login_form_validation_error(self):
        """Le formulaire invalide empêche l'authentification"""
        data = {"email": "", "password": ""}

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_session_is_created_after_login(self):
        """La session Django est bien créée après la connexion"""
        self.client.post(self.url, {"email": self.email, "password": self.password})

        # Vérifie que l'ID utilisateur est stocké en session
        session = self.client.session
        self.assertIn("_auth_user_id", session)
