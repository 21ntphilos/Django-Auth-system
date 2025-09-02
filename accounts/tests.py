from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAccountTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.password_reset_url = reverse("reset-password")
        self.forgot_password_url = reverse("forgot-password")

        self.user_data = {
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "strongpassword123",
        }

    def test_register_user_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url,self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["email"], self.user_data["email"])

    def test_register_user_duplicate_email(self):
        """Test registering with duplicate email fails"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_register_user_empty_fields(self):
        """Test empty fields validation"""
        response = self.client.post(self.register_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_login_user_success(self):
        """Test login with valid credentials"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_invalid_credentials(self):
        """Test login fails with wrong password"""
        User.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            "email": self.user_data["email"],
            "password": "wrongpassword"
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forgot_password_request(self):
        """Test requesting forgot password request"""
        user = User.objects.create_user(**self.user_data)

        forgotpassword_response = self.client.post(self.forgot_password_url, {
            "email": self.user_data["email"]
        }, format="json")
        token = forgotpassword_response.data.get("token", "")

        self.assertIn(forgotpassword_response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])
        self.assertTrue(token)

        response = self.client.post(self.password_reset_url, {
            "token": token,
            "new_password": "newpassword123"
        }, format="json")
       
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

        login_response = self.client.post(self.login_url, {
            "email": self.user_data["email"],
            "password": "newpassword123"
        }, format="json")
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

# Create your tests here.
