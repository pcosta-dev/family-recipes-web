import os

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker

from users.serializers import (
    CustomUserSerializer,
    ProfileImageSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()
fake = Faker()


@pytest.mark.django_db()
class TestCustomUserSerializer:
    def test_custom_user_serializer_valid_data(self):
        # Test if the serializer handles valid data correctly.
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
        }

        serializer = CustomUserSerializer(data=data)

        assert serializer.is_valid()

    def test_custom_user_serializer_invalid_data(self):
        # Test invalid data (e.g., missing required fields)
        data = {
            "username": fake.user_name(),
        }

        serializer = CustomUserSerializer(data=data)

        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestUserRegistrationSerializer:
    def test_user_registration_valid_data(self):
        # # Test if serializer handles valid data correctly.
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        serializer = UserRegistrationSerializer(data=data)

        assert serializer.is_valid()

    def test_user_registration_invalid_data(self):
        # Test invalid data (e.g., missing required fields)
        data = {
            "username": fake.user_name(),
        }

        serializer = UserRegistrationSerializer(data=data)

        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestUserLoginSerializer:
    def test_user_login_valid_credentials(self, user_with_abc123_password):
        # Test if serializer handles valid login credentials correctly.
        data = {
            "email": user_with_abc123_password.email,
            "password": "abc123",
        }

        serializer = UserLoginSerializer(data=data)

        assert serializer.is_valid()

    def test_user_login_invalid_credentials(self, user_with_abc123_password):
        # Test invalid login credentials (e.g., invalid password)
        data = {
            "email": user_with_abc123_password.email,
            "password": "wrongpassword",
        }

        serializer = UserLoginSerializer(data=data)

        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestProfileSerializer:
    def test_profile_serializer(self):
        # Test if serializer handles valid data correctly.
        serializer_data = {
            "birthday": fake.date_of_birth(minimum_age=30),
            "created_on": fake.date_time_this_decade(),
        }

        serializer = ProfileSerializer(data=serializer_data)

        assert serializer.is_valid()

    def test_profile_serializer_invalid_data(self):
        # Test invalid data (e.g., wrong format fields)
        data = {
            "birthday": "1980-Jan-01",
        }

        serializer = ProfileSerializer(data=data)

        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestProfileImageSerializer:
    def test_profile_image_serializer_valid_data(self):
        # Test if serializer handles valid data correctly.
        image_path = os.path.join(os.path.dirname(__file__), "test_profile_icon.jpg")
        file = SimpleUploadedFile(
            name="test_profile_icon.jpg",
            content=open(image_path, "rb").read(),
        )

        serializer_data = {
            "profile_img": file,
        }

        serializer = ProfileImageSerializer(data=serializer_data)

        assert serializer.is_valid()

    def test_profile_image_serializer_invalid_data(self):
        # Test invalid data (e.g., missing required fields/invalid data)
        data = {
            "profile_img": fake.email(),
        }

        serializer = ProfileImageSerializer(data=data)

        assert not serializer.is_valid()
