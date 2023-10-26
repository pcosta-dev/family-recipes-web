import factory
from users.models import CustomUser, Profile
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        skip_postgeneration_save=True
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.Faker('password')

    profile = factory.RelatedFactory(
        'users.tests.factories.ProfileFactory', factory_related_name='user')


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory, profile=None)
