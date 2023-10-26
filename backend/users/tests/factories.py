import factory
from users.models import CustomUser, Profile


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(CustomUserFactory)
