import factory
from faker import Faker
from users.models import CustomUser, Profile
from django.db.models.signals import post_save


fake = Faker()


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save = True

    username = fake.user_name()
    email = fake.email()
    password = fake.password()

    profile = factory.RelatedFactory(
        "users.tests.factories.ProfileFactory", factory_related_name="user"
    )


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
