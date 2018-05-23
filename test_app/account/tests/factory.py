# coding=utf-8
from faker import Faker
from utils.tests.factory import custom_factory

from ..models.account import User

fake = Faker()


class UserFactory(custom_factory.DjangoModelFactory):
    class Meta:
        model = User

    username = custom_factory.Faker('system_user_username')
    password = 'toor'
    email = custom_factory.Faker('system_user_email')
