import pytest


@pytest.mark.django_db()
class TestCustomUserModel:
    def test_string_representation(self, custom_user):
        # Test the string representation of CustomUser.
        assert str(custom_user) == custom_user.email


@pytest.mark.django_db()
class TestProfileModel:
    def test_profile_string_representation(self, base_custom_profile):
        # Test the string representation of Profile
        assert str(base_custom_profile) == base_custom_profile.user.username
