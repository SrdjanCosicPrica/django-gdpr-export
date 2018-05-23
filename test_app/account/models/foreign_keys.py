# coding=utf-8
from django.db import models

from ..models.account import User


class FKSetModel(models.Model):
    user = models.ForeignKey(User)


class ForeignKeyModel(models.Model):
    user = models.ForeignKey(User, related_name='fk_models')
    number_value = models.IntegerField(default=0)
