from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User


class AuthExtraEndpointsTest(APITestCase):
    def setUp(self):
        self.register_url = "/api/auth/users/"
        self.login_url = "/api/auth/jwt/create/"
        self.refresh_url = "/api/auth/jwt/refresh/"
        self.activation_url = "/api/auth/users/activation/"
        self.reset_password_url = "/api/auth/users/reset_password/"

        self.user_data = {
            "username": "janedoe",
            "email": "janedoe@example.com",
            "password": "SecurePass123",
            "re_password": "SecurePass123"
        }

        self.client.post(self.register_url, self.user_data, format="json")

    def test_token_refresh(self):
        login = self.client.post(self.login_url, {
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        }, format="json")

        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", login.data)

        refresh_token = login.data["refresh"]
        response = self.client.post(self.refresh_url, {"refresh": refresh_token}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_reset_password(self):
        response = self.client.post(self.reset_password_url, {
            "email": self.user_data["email"]
        }, format="json")
        self.assertIn(response.status_code, [200, 201, 204])  # Depends on implementation

    def test_activation_endpoint_format(self):
        response = self.client.post(self.activation_url, {
            "uid": "fakeuid",
            "token": "faketoken"
        }, format="json")
        self.assertIn(response.status_code, [400, 403])
