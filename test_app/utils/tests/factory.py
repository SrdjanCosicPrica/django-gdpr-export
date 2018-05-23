# coding=utf-8
import factory
from faker.providers import BaseProvider

from account.models.account import User

custom_factory = factory


class UserProvider(BaseProvider):
    def username(self):
        unique = False
        while not unique:
            username = custom_factory.Faker('user_name').generate({})
            qs = User.objects.filter(username=username)
            if qs.count() == 0:
                return username

    def user_email(self):
        unique = False
        while not unique:
            email = custom_factory.Faker('safe_email').generate({})
            qs = User.objects.filter(email=email)
            if qs.count() == 0:
                return email


custom_factory.Faker.add_provider(UserProvider)
