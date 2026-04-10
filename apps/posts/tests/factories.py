import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from ..models import Post

CustomUser = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    is_writer = True  # Set default to True for testing convenience


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    content = factory.Faker("paragraph")
    author = factory.SubFactory(UserFactory)
