import pytest
from faker import Faker
from .factories import UserFactory, ProfileFactory


fake = Faker()


@pytest.fixture()
def custom_user():
    return UserFactory()#username=fake.user_name(), email=fake.email(), password=fake.password())


@pytest.fixture()
def base_custom_profile():
    return ProfileFactory()
