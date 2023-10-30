import json

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

fake = Faker()
User = get_user_model()


@pytest.mark.django_db()
class TestUserRegistrationAPIView:
    def test_register_user(self, client):
        url = reverse("users:create-user")
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1

    def test_register_user_duplicate_email(self, client, custom_user):
        # Retrieve the email of an existing user
        existing_email = custom_user.email
        url = reverse("users:create-user")

        # Try to create a user with an already used email address
        data = {
            "username": fake.user_name(),
            "email": existing_email,
            "password": fake.password(),
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_409_CONFLICT
        response_error = json.loads(response.content).get("error")
        assert response_error == "User with this email already exists."


@pytest.mark.django_db()
class TestUserLoginAPIView:
    def test_invalid_login(self, client, user_with_abc123_password):
        url = reverse("users:login-user")
        data = {
            "email": user_with_abc123_password.email,
            "password": "123abc",
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        response_error = json.loads(response.content).get("error")
        assert response_error == "Incorrect credentials"

    def test_login_user(self, client, user_with_abc123_password):
        url = reverse("users:login-user")
        data = {
            "email": user_with_abc123_password.email,
            "password": "abc123",
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db()
class TestUserLogoutAPIView:
    def test_user_logout(self, client, user_with_abc123_password):
        # Log in the user to obtain authentication tokens
        user = User.objects.get(email=user_with_abc123_password.email)
        login_successful = client.login(username=user.email, password="abc123")
        assert login_successful is True

        # Extract the token
        refresh_token = RefreshToken.for_user(user)

        # Use the refresh token to make a request to the logout view
        logout_url = reverse("users:logout-user")
        logout_data = {"refresh": str(refresh_token)}
        logout_response = client.post(logout_url, logout_data, format="json")

        # Verify that the logout request returns the expected response
        assert logout_response.status_code == status.HTTP_204_NO_CONTENT

    def test_logout_with_invalid_refresh_token(self, client, user_with_abc123_password):
        # Attempt to log out with an invalid refresh token
        user = User.objects.get(email=user_with_abc123_password.email)
        client.login(username=user.email, password="abc123")

        logout_url = reverse("users:logout-user")
        logout_data = {"refresh": "invalid_refresh_token"}
        logout_response = client.post(logout_url, logout_data, format="json")

        # Verify that the logout request returns the expected response for an invalid token
        assert logout_response.status_code == status.HTTP_400_BAD_REQUEST

    def test_logout_without_refresh_token(self, client, user_with_abc123_password):
        # Log in the user to obtain authentication tokens
        user = User.objects.get(email=user_with_abc123_password.email)
        client.login(username=user.email, password="abc123")

        # Attempt to log out without providing a refresh token
        logout_url = reverse("users:logout-user")
        logout_response = client.post(logout_url, format="json")

        # Verify that the logout request returns the expected response for missing token
        assert logout_response.status_code == status.HTTP_400_BAD_REQUEST
