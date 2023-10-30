import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.mark.django_db()
class TestUserManager:
    def test_create_valid_user(self):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        assert user.username == username
        assert user.email == email
        assert check_password(password, user.password)
        assert user.is_active
        assert not user.is_superuser
        assert not user.is_staff

    def test_create_user_missing_arguments(self):
        email = fake.email()
        password = fake.password()

        with pytest.raises(TypeError) as ex_info:
            User.objects.create_user()

        expected_message = (
            "CustomUserManager.create_user() missing 2 "
            "required positional arguments: 'email' and 'password'"
        )
        assert str(ex_info.value) == expected_message

        with pytest.raises(TypeError) as ex_info:
            User.objects.create_user(email=email)

        expected_message = (
            "CustomUserManager.create_user() missing 1 "
            "required positional argument: 'password'"
        )
        assert str(ex_info.value) == expected_message

        with pytest.raises(TypeError) as ex_info:
            User.objects.create_user(password=password)

        expected_message = (
            "CustomUserManager.create_user() missing 1 "
            "required positional argument: 'email'"
        )

        assert str(ex_info.value) == expected_message

    def test_create_superuser(self):
        email = fake.email()
        password = fake.password()
        user = User.objects.create_super_user(email=email, password=password)

        assert user.email == email
        assert check_password(password, user.password)
        assert user.is_active
        assert user.is_superuser
        assert user.is_staff

        with pytest.raises(ValueError) as ex_info:
            User.objects.create_super_user(
                email=email, password=password, is_superuser=False
            )

        expected_message = "Superuser must have is_superuser=True"
        assert str(ex_info.value) == expected_message

        with pytest.raises(ValueError) as ex_info:
            User.objects.create_super_user(
                email=email, password=password, is_staff=False
            )

        expected_message = "Superuser must have is_staff=True"
        assert str(ex_info.value) == expected_message
