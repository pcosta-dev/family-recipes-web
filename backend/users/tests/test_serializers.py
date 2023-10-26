import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status

fake = Faker()
User = get_user_model()


@pytest.mark.django_db()
class TestUserRegistrationSerializer:
    def test_register_user(self, client):
        url = reverse('users:create-user')
        data = {
            'username': fake.user_name(),
            'email': fake.email(),
            'password': fake.password(),
        }
        
        response = client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1