import pytest
from faker import Faker
from .factories import CustomUserFactory, ProfileFactory


fake = Faker()


@pytest.fixture()
def custom_user():
    return CustomUserFactory(email=fake.email(), password=fake.password())


@pytest.fixture()
def base_custom_profile(custom_user):
    return ProfileFactory(user=custom_user, username=fake.name())
