import pytest
import os
from faker import Faker
from users.models import Profile
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from users.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    CustomUserSerializer,
    ProfileSerializer,
    ProfileImageSerializer,
)

User = get_user_model()
fake = Faker()


@pytest.mark.django_db()
class TestCustomUserSerializer:
    def test_custom_user_serializer_valid_data(self):
        # Create a CustomUser instance (or use a factory)
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
        }

        serializer = CustomUserSerializer(data=data)

        # Check if the serialized data is valid
        assert serializer.is_valid()

    def test_custom_user_serializer_invalid_data(self):
        # Create invalid test data (e.g., missing required fields)
        data = {
            "username": fake.user_name(),
        }

        serializer = CustomUserSerializer(data=data)

        # Check if data is not valid
        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestUserRegistrationSerializer:
    def test_user_registration_valid_data(self):
        # Create test data
        data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": fake.password(),
        }

        serializer = UserRegistrationSerializer(data=data)

        # Check if data is valid
        assert serializer.is_valid()

    def test_user_registration_invalid_data(self):
        # Create invalid test data (e.g., missing required fields)
        data = {
            "username": fake.user_name(),
        }

        serializer = UserRegistrationSerializer(data=data)

        # Check if data is not valid
        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestUserLoginSerializer:
    def test_user_login_valid_credentials(self, user_with_abc123_password):
        data = {
            "email": user_with_abc123_password.email,
            "password": "abc123",
        }

        serializer = UserLoginSerializer(data=data)

        # Check if data is valid
        assert serializer.is_valid()

    def test_user_login_invalid_credentials(self, user_with_abc123_password):
        data = {
            "email": user_with_abc123_password.email,
            "password": "wrongpassword",
        }

        serializer = UserLoginSerializer(data=data)

        # Check if data is not valid
        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestProfileSerializer:
    def test_profile_serializer(self):
        # Create a Profile instance (or use a factory)
        serializer_data = {
            "birthday": fake.date_of_birth(minimum_age=30),
            "created_on": fake.date_time_this_decade(),
        }

        # Create a serializer instance with the data
        serializer = ProfileSerializer(data=serializer_data)

        # Check if the serialized data is valid
        assert serializer.is_valid()

    def test_profile_serializer_invalid_data(self):
        # Create invalid test data (e.g., wrong format fields)
        data = {
            "birthday": "1980-Jan-01",
        }

        serializer = ProfileSerializer(data=data)

        # Check if the serializer is not valid
        assert not serializer.is_valid()


@pytest.mark.django_db()
class TestProfileImageSerializer:
    def test_profile_image_serializer_valid_data(self):
        image_path = os.path.join(os.path.dirname(__file__), "test_profile_icon.jpg")
        file = SimpleUploadedFile(
            name="test_profile_icon.jpg",
            content=open(image_path, "rb").read(),
        )
        # Create a Profile instance (or use a factory) with a profile image
        serializer_data = {
            "profile_img": file,
        }

        serializer = ProfileImageSerializer(data=serializer_data)

        # Check if the serialized data is valid
        serializer.is_valid()
        print(serializer.errors, serializer_data)
        assert serializer.is_valid()

    def test_profile_image_serializer_invalid_data(self):
        # Create invalid test data (e.g., missing required fields/invalid data)
        data = {
            "profile_img": fake.email(),
        }

        serializer = ProfileImageSerializer(data=data)

        # Check if data is not valid
        assert not serializer.is_valid()
