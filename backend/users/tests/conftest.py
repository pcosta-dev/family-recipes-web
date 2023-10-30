import pytest
from .factories import UserFactory, ProfileFactory
from django.contrib.auth import get_user_model


@pytest.fixture()
def custom_user():
    return UserFactory()


@pytest.fixture()
def user_with_abc123_password():
    return get_user_model().objects.create_user(
        email="test@example.com",
        password="abc123",
    )


@pytest.fixture()
def base_custom_profile():
    return ProfileFactory()
