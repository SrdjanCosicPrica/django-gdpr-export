# coding=utf-8
from django.db import models

from ..models.account import User


class M2MSetModel(models.Model):
    user = models.ManyToManyField(User)


class ManyToManyModel(models.Model):
    user = models.ManyToManyField(User, related_name='m2m_models')
    text_value = models.CharField(max_length=1)
